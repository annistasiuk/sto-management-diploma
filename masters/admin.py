from django.contrib import admin
from .models import Master


@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'specialization', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('full_name', 'phone', 'specialization')