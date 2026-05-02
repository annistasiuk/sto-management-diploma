from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Client
from .forms import ClientForm


def client_list_view(request):
    query = request.GET.get('q', '')

    clients = Client.objects.all().order_by('-created_at')

    if query:
        clients = clients.filter(
            Q(full_name__icontains=query) |
            Q(phone__icontains=query) |
            Q(email__icontains=query)
        )

    return render(request, 'clients/client_list.html', {
        'clients': clients,
        'query': query
    })


def client_detail_view(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    cars = client.cars.all().order_by('-created_at')

    return render(request, 'clients/client_detail.html', {
        'client': client,
        'cars': cars
    })


def edit_client_view(request, client_id):
    client = get_object_or_404(Client, id=client_id)

    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)

        if form.is_valid():
            form.save()
            messages.success(request, 'Дані клієнта успішно оновлено.')
            return redirect('client_detail', client_id=client.id)
    else:
        form = ClientForm(instance=client)

    return render(request, 'clients/edit_client.html', {
        'form': form,
        'client': client
    })


def delete_client_view(request, client_id):
    client = get_object_or_404(Client, id=client_id)

    if request.method == 'POST':
        client.delete()
        messages.success(request, 'Клієнта успішно видалено.')
        return redirect('client_list')

    return render(request, 'clients/client_confirm_delete.html', {
        'client': client
    })