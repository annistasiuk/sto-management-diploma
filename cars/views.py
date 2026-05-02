from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Car
from .forms import CarForm
from clients.models import Client



def car_list_view(request):
    query = request.GET.get('q', '')

    cars = Car.objects.select_related('owner').all().order_by('-created_at')

    if query:
        cars = cars.filter(
            Q(make__icontains=query) |
            Q(model_name__icontains=query) |
            Q(license_plate__icontains=query) |
            Q(owner_name__icontains=query) |
            Q(owner__full_name__icontains=query) |
            Q(owner__phone__icontains=query)
        )

    return render(request, 'cars/car_list.html', {
        'cars': cars,
        'query': query
    })


def car_detail_view(request, car_id):
    car = get_object_or_404(
        Car.objects.select_related('owner'),
        id=car_id
    )

    repairs = car.repairs.all().order_by('-created_at')

    return render(request, 'cars/car_detail.html', {
        'car': car,
        'repairs': repairs
    })


def edit_car_view(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES, instance=car)

        if form.is_valid():
            car = form.save(commit=False)

            owner_phone = form.cleaned_data.get('owner_phone', '')
            owner_name = form.cleaned_data.get('owner_name', '')

            if owner_phone:
                if car.owner:
                    car.owner.full_name = owner_name
                    car.owner.phone = owner_phone
                    car.owner.save()
                else:
                    client, created = Client.objects.get_or_create(
                        phone=owner_phone,
                        defaults={'full_name': owner_name}
                    )

                    if not created:
                        client.full_name = owner_name
                        client.save()

                    car.owner = client

            car.save()

            messages.success(request, 'Дані автомобіля успішно оновлено.')
            return redirect('car_detail', car_id=car.id)

    else:
        form = CarForm(instance=car)

    return render(request, 'cars/edit_car.html', {
        'form': form,
        'car': car
    })


def delete_car_view(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    if request.method == 'POST':
        car.delete()
        messages.success(request, 'Автомобіль успішно видалено.')
        return redirect('car_list')

    return render(request, 'cars/car_confirm_delete.html', {
        'car': car
    })