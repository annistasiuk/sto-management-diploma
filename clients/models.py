from django.db import models


class Client(models.Model):
    full_name = models.CharField(max_length=150, verbose_name="ПІБ")
    phone = models.CharField(max_length=20, unique=True, verbose_name="Телефон")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name="Адреса")
    notes = models.TextField(blank=True, null=True, verbose_name="Примітки")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Клієнт"
        verbose_name_plural = "Клієнти"
        ordering = ['full_name']