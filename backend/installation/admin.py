from django.contrib import admin
from .models import Installation, InstallationType

@admin.register(Installation)
class InstallationAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'type', 'description', 'availability']
    search_fields = ['name', 'type__name']

@admin.register(InstallationType)
class InstallationTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'image']
    search_fields = ['name']