from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Q
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from repairs.models import Repair
from masters.models import Master


def is_admin(user):
    return user.is_superuser or user.groups.filter(name='Admin').exists()


def is_manager(user):
    return user.groups.filter(name='Manager').exists()


def is_master(user):
    return user.groups.filter(name='Master').exists()


def user_login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    error = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('home')

        error = 'Невірний логін або пароль'

    return render(request, 'login.html', {
        'error': error
    })


def user_logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def home_view(request):
    status_filter = request.GET.get('status', '')

    repairs_queryset = Repair.objects.select_related(
        'car',
        'car__owner',
        'master'
    )

    if is_master(request.user) and not is_admin(request.user) and not is_manager(request.user):
        try:
            master_profile = request.user.master_profile
            repairs_queryset = repairs_queryset.filter(master=master_profile)
        except Master.DoesNotExist:
            repairs_queryset = repairs_queryset.none()

    active_repairs = repairs_queryset.filter(
        status__in=['new', 'in_progress']
    ).count()

    awaiting_parts = repairs_queryset.filter(
        status='awaiting_parts'
    ).count()

    completed_repairs = repairs_queryset.filter(
        status__in=['completed', 'issued']
    ).count()

    today_repairs = repairs_queryset.filter(
        created_at__date=timezone.now().date()
    ).count()

    unassigned_repairs = repairs_queryset.filter(
        master__isnull=True,
        status__in=['new', 'in_progress', 'awaiting_parts']
    ).count()

    latest_repairs = repairs_queryset.order_by('-created_at')

    if status_filter:
        latest_repairs = latest_repairs.filter(status=status_filter)

    latest_repairs = latest_repairs[:8]

    today = timezone.now().date()

    for repair in latest_repairs:
        repair.is_overdue = False
        repair.is_today_deadline = False

        if repair.planned_end_date:
            if repair.planned_end_date < today:
                repair.is_overdue = True
            elif repair.planned_end_date == today:
                repair.is_today_deadline = True

    master_workload = Master.objects.filter(
        is_active=True
    ).annotate(
        active_repairs_count=Count(
            'repairs',
            filter=Q(
                repairs__status__in=[
                    'new',
                    'in_progress',
                    'awaiting_parts'
                ]
            )
        )
    ).order_by('full_name')

    if is_master(request.user) and not is_admin(request.user) and not is_manager(request.user):
        master_workload = master_workload.filter(user=request.user)

    context = {
        'active_repairs': active_repairs,
        'awaiting_parts': awaiting_parts,
        'completed_repairs': completed_repairs,
        'today_repairs': today_repairs,
        'unassigned_repairs': unassigned_repairs,
        'latest_repairs': latest_repairs,
        'master_workload': master_workload,
        'is_admin': is_admin(request.user),
        'is_manager': is_manager(request.user),
        'is_master': is_master(request.user),
    }

    return render(request, 'home.html', context)


@login_required
def update_repair_status_view(request, repair_id, status):
    repair = get_object_or_404(Repair, id=repair_id)

    if is_master(request.user) and not is_admin(request.user) and not is_manager(request.user):
        try:
            master_profile = request.user.master_profile
        except Master.DoesNotExist:
            messages.error(request, 'До вашого користувача не привʼязано майстра.')
            return redirect('home')

        if repair.master != master_profile:
            messages.error(request, 'Ви можете змінювати тільки свої ремонти.')
            return redirect('home')

    allowed_statuses = [
        Repair.Status.NEW,
        Repair.Status.IN_PROGRESS,
        Repair.Status.AWAITING_PARTS,
        Repair.Status.COMPLETED,
        Repair.Status.ISSUED,
        Repair.Status.CANCELLED,
    ]

    if status in allowed_statuses:
        repair.status = status
        repair.save()
        messages.success(request, 'Статус ремонту оновлено.')

    return redirect('home')