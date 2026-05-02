from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator
from clients.models import Client
import datetime


class Car(models.Model):

    class Transmission(models.TextChoices):
        MANUAL = 'manual', 'Механічна'
        AUTOMATIC = 'automatic', 'Автоматична'
        ROBOT = 'robot', 'Роботизована'
        VARIATOR = 'variator', 'Варіатор'

    class FuelType(models.TextChoices):
        PETROL = 'petrol', 'Бензин'
        DIESEL = 'diesel', 'Дизель'
        ELECTRIC = 'electric', 'Електро'
        HYBRID = 'hybrid', 'Гібрид'
        GAS = 'gas', 'Газ'

    owner = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='cars',
        verbose_name="Власник",
        null=True,
        blank=True
    )

    make = models.CharField(
        max_length=100,
        verbose_name="Марка"
    )

    model_name = models.CharField(
        max_length=100,
        verbose_name="Модель"
    )

    license_plate = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Держномер"
    )

    vin = models.CharField(
        max_length=17,
        unique=True,
        verbose_name="VIN-код",
        validators=[MinLengthValidator(17)]
    )

    owner_name = models.CharField(
        max_length=100,
        verbose_name="ПІБ власника",
        blank=True
    )

    year = models.PositiveIntegerField(
        verbose_name="Рік випуску",
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(datetime.date.today().year + 1)
        ],
        help_text="Використовуйте формат: <YYYY>"
    )

    color = models.CharField(
        max_length=50,
        verbose_name="Колір"
    )

    transmission = models.CharField(
        max_length=20,
        choices=Transmission.choices,
        default=Transmission.AUTOMATIC,
        verbose_name="Коробка передач"
    )

    fuel_type = models.CharField(
        max_length=20,
        choices=FuelType.choices,
        default=FuelType.PETROL,
        verbose_name="Тип пального"
    )

    mileage = models.PositiveIntegerField(
        default=0,
        verbose_name="Пробіг (км)"
    )

    engine_volume = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        blank=True,
        null=True,
        verbose_name="Об'єм двигуна (л)"
    )

    description = models.TextField(
        blank=True,
        verbose_name="Опис"
    )

    main_image = models.ImageField(
        upload_to='cars/%Y/%m/',
        blank=True,
        null=True,
        verbose_name="Фото"
    )

    is_published = models.BooleanField(
        default=True,
        verbose_name="Опубліковано"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата додавання"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата оновлення"
    )

    class Meta:
        verbose_name = "Автомобіль"
        verbose_name_plural = "Автомобілі"
        ordering = ['-created_at']

    def __str__(self):
        plate = f" {self.license_plate}" if self.license_plate else ""
        return f"{self.make} {self.model_name}{plate}"