from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

from .models import Repair
from .forms import RepairForm
from cars.models import Car
from masters.models import Master


def is_admin(user):
    return user.is_superuser or user.groups.filter(name='Admin').exists()


def is_manager(user):
    return user.groups.filter(name='Manager').exists()


def is_master(user):
    return user.groups.filter(name='Master').exists()


def get_master_profile(user):
    try:
        return user.master_profile
    except Master.DoesNotExist:
        return None


def can_access_repair(user, repair):
    if is_admin(user) or is_manager(user):
        return True

    if is_master(user):
        master_profile = get_master_profile(user)
        return master_profile is not None and repair.master == master_profile

    return False


@login_required
def repair_list_view(request):
    query = request.GET.get('q', '')
    status_filter = request.GET.get('status', '')

    repairs = Repair.objects.select_related(
        'car',
        'car__owner',
        'master'
    ).order_by('-created_at')

    if is_master(request.user) and not is_admin(request.user) and not is_manager(request.user):
        master_profile = get_master_profile(request.user)

        if master_profile:
            repairs = repairs.filter(master=master_profile)
        else:
            repairs = repairs.none()

    if query:
        repairs = repairs.filter(
            Q(car__make__icontains=query) |
            Q(car__model_name__icontains=query) |
            Q(car__license_plate__icontains=query) |
            Q(car__owner__full_name__icontains=query) |
            Q(car__owner_name__icontains=query) |
            Q(problem_description__icontains=query) |
            Q(master__full_name__icontains=query)
        )

    if status_filter:
        repairs = repairs.filter(status=status_filter)

    return render(request, 'repairs/repair_list.html', {
        'repairs': repairs,
        'query': query,
        'current_filter': status_filter,
        'status_choices': Repair.Status.choices,
        'is_admin': is_admin(request.user),
        'is_manager': is_manager(request.user),
        'is_master': is_master(request.user),
    })


@login_required
def add_repair_view(request):
    if is_master(request.user) and not is_admin(request.user) and not is_manager(request.user):
        messages.error(request, 'Майстер не може створювати нові заявки.')
        return redirect('home')

    if request.method == 'POST':
        form = RepairForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Ремонтну заявку створено.')
            return redirect('repair_list')

        messages.error(request, 'Перевірте правильність заповнення форми.')
    else:
        form = RepairForm()

    return render(request, 'repairs/add_repair.html', {
        'form': form
    })


@login_required
def add_repair_for_car_view(request, car_id):
    if is_master(request.user) and not is_admin(request.user) and not is_manager(request.user):
        messages.error(request, 'Майстер не може створювати нові заявки.')
        return redirect('home')

    car = get_object_or_404(Car, id=car_id)

    if request.method == 'POST':
        form = RepairForm(request.POST)

        if form.is_valid():
            repair = form.save(commit=False)
            repair.car = car
            repair.save()

            messages.success(request, 'Ремонт створено.')
            return redirect('repair_list')

        messages.error(request, 'Перевірте правильність заповнення форми.')
    else:
        form = RepairForm(initial={'car': car})

    return render(request, 'repairs/add_repair.html', {
        'form': form,
        'selected_car': car
    })


@login_required
def edit_repair_view(request, repair_id):
    repair = get_object_or_404(
        Repair.objects.select_related('car', 'car__owner', 'master'),
        id=repair_id
    )

    if not can_access_repair(request.user, repair):
        messages.error(request, 'Ви можете редагувати тільки свої ремонти.')
        return redirect('home')

    if request.method == 'POST':
        form = RepairForm(request.POST, request.FILES, instance=repair)

        if form.is_valid():
            repair = form.save(commit=False)

            if request.FILES.get('main_image'):
                repair.car.main_image = request.FILES.get('main_image')
                repair.car.save()

            repair.save()
            messages.success(request, 'Зміни успішно збережено.')
            return redirect('repair_list')

        messages.error(request, 'Перевірте правильність заповнення форми.')
    else:
        form = RepairForm(instance=repair)

    return render(request, 'repairs/edit_repair.html', {
        'form': form,
        'repair': repair
    })


@login_required
def delete_repair_view(request, repair_id):
    if is_master(request.user) and not is_admin(request.user) and not is_manager(request.user):
        messages.error(request, 'Майстер не може видаляти ремонти.')
        return redirect('home')

    repair = get_object_or_404(Repair, id=repair_id)
    repair.delete()

    messages.success(request, 'Ремонт видалено.')
    return redirect('repair_list')


@login_required
def repair_pdf_view(request, repair_id):
    repair = get_object_or_404(
        Repair.objects.select_related('car', 'car__owner', 'master'),
        id=repair_id
    )

    if not can_access_repair(request.user, repair):
        messages.error(request, 'Ви можете переглядати PDF тільки своїх ремонтів.')
        return redirect('home')

    car_name = f'{repair.car.make}_{repair.car.model_name}'.replace(' ', '_')
    plate = repair.car.license_plate.replace(' ', '') if repair.car.license_plate else 'without_number'
    filename = f'STO_Check_{car_name}_{plate}.pdf'

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    pdf = canvas.Canvas(response, pagesize=A4)
    _, height = A4

    font_paths = [
        '/System/Library/Fonts/Supplemental/Arial Unicode.ttf',
        '/Library/Fonts/Arial Unicode.ttf',
        '/System/Library/Fonts/Supplemental/Arial.ttf',
    ]

    font_name = 'Helvetica'

    for font_path in font_paths:
        try:
            pdfmetrics.registerFont(TTFont('UAFont', font_path))
            font_name = 'UAFont'
            break
        except Exception:
            continue

    pdf.setFont(font_name, 18)

    y = height - 60

    pdf.drawString(50, y, 'СТО Менеджер')
    y -= 30

    pdf.setFont(font_name, 13)
    pdf.drawString(50, y, f'Квитанція ремонту №{repair.id}')
    y -= 30

    pdf.drawString(
        50,
        y,
        f'Дата створення: {repair.created_at.strftime("%d.%m.%Y %H:%M")}'
    )
    y -= 40

    def draw_row(label, value):
        nonlocal y
        pdf.drawString(50, y, label)
        pdf.drawString(220, y, str(value) if value else 'Не вказано')
        y -= 25

    draw_row('Автомобіль:', f'{repair.car.make} {repair.car.model_name}')
    draw_row('Держномер:', repair.car.license_plate)
    draw_row('VIN-код:', repair.car.vin)
    draw_row('Рік випуску:', repair.car.year)

    y -= 15

    owner_name = repair.car.owner.full_name if repair.car.owner else repair.car.owner_name
    owner_phone = repair.car.owner.phone if repair.car.owner and repair.car.owner.phone else 'Не вказано'

    draw_row('Клієнт:', owner_name)
    draw_row('Телефон:', owner_phone)

    y -= 15

    draw_row('Опис:', repair.problem_description[:70])
    draw_row('Майстер:', repair.master.full_name if repair.master else 'Не призначено')
    draw_row('Статус:', repair.get_status_display())
    draw_row('Вартість робіт:', f'{repair.labor_cost} грн')
    draw_row('Вартість запчастин:', f'{repair.parts_cost} грн')

    y -= 15

    pdf.setFont(font_name, 15)
    pdf.drawString(50, y, f'Загальна сума: {repair.total_cost} грн')

    y -= 60

    pdf.setFont(font_name, 11)
    pdf.drawString(50, y, 'Підпис майстра: ____________________')
    pdf.drawString(300, y, 'Підпис клієнта: ____________________')

    pdf.showPage()
    pdf.save()

    return response


@login_required
def repair_receipt_pdf_view(request, repair_id):
    return repair_pdf_view(request, repair_id)