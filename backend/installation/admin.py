from django.contrib import admin
from .models import Installation, InstallationType, AvailableHour

@admin.register(Installation)
class InstallationAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'type', 'description', 'availability']
    search_fields = ['id', 'name', 'type__name']

@admin.register(InstallationType)
class InstallationTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'image']
    search_fields = ['name']

@admin.register(AvailableHour)
class AvailableHourAdmin(admin.ModelAdmin):
    list_display = ['installation', 'day_of_week', 'start_time', 'end_time']
    search_fields = ['installation__name', 'day_of_week']