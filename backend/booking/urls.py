from django.urls import path
from . import views

urlpatterns = [
    path('booking/scheduled', views.get_scheduled_bookings, name='get_scheduled_bookings'),
    path('booking/<int:booking_id>', views.get_booking, name='get_booking'),
    path('', views.create_booking, name='create_booking'),
    path('cancel/<int:booking_id>', views.cancel_booking, name='cancel_booking'),
    path('<int:booking_id>', views.delete_booking, name='delete_booking'),   
]