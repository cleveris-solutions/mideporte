from django.urls import path
from . import views

urlpatterns = [
    path('booking/scheduled', views.get_scheduled_bookings, name='get_scheduled_bookings'),
    path('booking/<int:booking_id>', views.get_booking, name='get_booking'),
    path('<str:dni>', views.get_bookings_by_user, name='get_bookings_by_user'),
    path('', views.create_booking, name='create_booking'),
    path('cancel/<int:booking_id>', views.cancel_booking, name='cancel_booking'), 
]