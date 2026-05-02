from django.db import models
from django.core.validators import MinValueValidator
from cars.models import Car
from masters.models import Master


class Repair(models.Model):

    class Status(models.TextChoices):
        NEW = 'new', 'Новий'
        IN_PROGRESS = 'in_progress', 'В роботі'
        AWAITING_PARTS = 'awaiting_parts', 'Очікує запчастини'
        COMPLETED = 'completed', 'Завершено'
        ISSUED = 'issued', 'Видано клієнту'
        CANCELLED = 'cancelled', 'Скасовано'

    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name='repairs',
        verbose_name="Автомобіль"
    )

    problem_description = models.TextField(
        verbose_name="Опис несправності"
    )

    work_description = models.TextField(
        blank=True,
        verbose_name="Виконані роботи"
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
        verbose_name="Статус ремонту"
    )

    master = models.ForeignKey(
        Master,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='repairs',
        verbose_name="Майстер"
    )

    start_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата прийому"
    )

    planned_end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Планова дата завершення"
    )

    end_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Фактична дата завершення"
    )

    labor_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Вартість робіт"
    )

    parts_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Вартість запчастин"
    )

    notes = models.TextField(
        blank=True,
        verbose_name="Примітки"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата створення"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата оновлення"
    )

    @property
    def total_cost(self):
        return self.labor_cost + self.parts_cost

    @property
    def client(self):
        return self.car.owner

    def __str__(self):
        return f"Ремонт №{self.id} — {self.car.make} {self.car.model_name}"

    class Meta:
        verbose_name = "Ремонтне замовлення"
        verbose_name_plural = "Ремонтні замовлення"
        ordering = ['-created_at']