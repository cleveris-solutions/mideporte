from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_booking, name='create_booking'),
    path('cancel/<int:booking_id>', views.cancel_booking, name='cancel_booking'),   
]