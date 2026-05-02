from django.test import TestCase
from django.urls import reverse
from .models import Car
from django.contrib import messages


class CarAppTests(TestCase):

    def test_add_car_success(self):
        url = reverse('add_car')
        response = self.client.post(url, {
            'make': 'Toyota',
            'model': 'Camry',
            'year': 2020,
            'vin': '1234567890ABCDEFG',
            'owner_name': 'Тест Тестенко',
            'owner_phone': '0501234567'
        }, follow=True)

        self.assertEqual(Car.objects.count(), 1)
        self.assertRedirects(response, reverse('car_list'))

        self.assertContains(response, 'Автомобіль успішно додано!')

        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.SUCCESS)

    def test_add_car_invalid_vin(self):
        url = reverse('add_car')
        response = self.client.post(url, {
            'make': 'TestMake',
            'model': 'TestModel',
            'year': 2010,
            'vin': 'SHORT_VIN',
            'owner_name': 'Тест Власник',
            'owner_phone': '0991234567'
        })

        self.assertEqual(Car.objects.count(), 0)
        self.assertContains(response, 'VIN-код повинен складатися з 17 символів')

    def test_add_car_invalid_year(self):
        url = reverse('add_car')
        response = self.client.post(url, {
            'make': 'Ford',
            'model': 'Mustang',
            'year': 1950,
            'vin': 'ANOTHERVIN123456789',
            'owner_name': 'Тест Форд',
            'owner_phone': '0671234567'
        })

        self.assertEqual(Car.objects.count(), 0)
        self.assertContains(response, 'Вкажіть коректний рік випуску')