from django.contrib import admin
from .models import Repair


@admin.register(Repair)
class RepairAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'car',
        'client',
        'status',
        'master',
        'total_cost',
        'start_date',
    )

    list_filter = (
        'status',
        'master',
        'start_date',
    )

    search_fields = (
        'car__make',
        'car__model_name',
        'car__vin',
        'car__license_plate',
        'car__owner__full_name',
        'car__owner_name',
        'master__full_name',
        'problem_description',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
        'total_cost',
    )