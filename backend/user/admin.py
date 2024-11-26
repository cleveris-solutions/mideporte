from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['DNI', 'email', 'name', 'surname', 'telephone_number', 'is_staff', 'is_active', 'suspended']
    search_fields = ['DNI', 'email', 'name', 'surname']