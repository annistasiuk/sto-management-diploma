from django.test import TestCase
from django.urls import reverse

class RepairPageTests(TestCase):
    def setUp(self):
        car1 = Car.objects.create(...)
        self.repair_new = Repair.objects.create(car=car1, description="Новий", status='new')
        self.repair_done = Repair.objects.create(car=car1, description="Зроблено", status='completed')

    def test_repair_list_displays_all(self):
        response = self.client.get(reverse('repair_list'))
        self.assertContains(response, 'Новий')
        self.assertContains(response, 'Зроблено')

    def test_repair_list_filter_by_status(self):
        url = reverse('repair_list') + '?status=completed'
        response = self.client.get(url)
        self.assertNotContains(response, 'Новий')
        self.assertContains(response, 'Зроблено')