from django.contrib import admin
from .models import Car


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = (
        'make',
        'model_name',
        'owner',
        'year',
        'fuel_type',
        'transmission',
        'mileage',
        'created_at'
    )

    search_fields = (
        'make',
        'model_name',
        'vin',
        'owner__full_name'
    )

    list_filter = (
        'fuel_type',
        'transmission',
        'year',
        'created_at'
    )

    list_per_page = 20