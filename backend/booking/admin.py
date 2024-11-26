from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'installation', 'start', 'status']
    search_fields = ['id', 'user__DNI', 'installation__name', 'status']