from django.test import TestCase
from django.core import mail
from django.urls import reverse
from django.contrib import messages

from cars.models import Car
from repairs.models import Repair


class BillingTests(TestCase):
    def setUp(self):
        self.car = Car.objects.create(
            make='TestMake',
            model='TestModel',
            year=2020,
            vin='TESTVIN1234567890',
            owner_name='Test Owner',
            owner_phone='1234567890'
        )
        self.repair = Repair.objects.create(
            car=self.car,
            description="Тестовий ремонт",
            status='completed'
        )

    def test_pdf_generation(self):
        url = reverse('generate_invoice', args=[self.repair.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')

    def test_email_sending(self):
        url = reverse('send_invoice', args=[self.repair.id])

        self.client.get(url)

        self.assertEqual(len(mail.outbox), 1)

        expected_subject = f"Рахунок за ремонт авто {self.car.make}"
        self.assertEqual(mail.outbox[0].subject, expected_subject)

        self.assertEqual(len(mail.outbox[0].attachments), 1)

    def test_send_email_success_message(self):
        url = reverse('send_invoice', args=[self.repair.id])
        response = self.client.get(url, follow=True)  # follow=True

        self.assertRedirects(response, reverse('repair_list'))

        self.assertContains(response, f'Рахунок для {self.car.make} успішно надіслано!')

        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.SUCCESS)