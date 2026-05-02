from django.db import models
from django.contrib.auth.models import User


class Master(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='master_profile',
        verbose_name='Користувач'
    )

    full_name = models.CharField(
        max_length=100,
        verbose_name="ПІБ майстра"
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Телефон"
    )

    specialization = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Спеціалізація"
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Активний"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата додавання"
    )

    class Meta:
        verbose_name = "Майстер"
        verbose_name_plural = "Майстри"
        ordering = ['full_name']

    def __str__(self):
        return self.full_name