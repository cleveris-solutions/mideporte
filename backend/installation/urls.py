from django.urls import path
from . import views

urlpatterns = [
    path('sports', views.sport_list, name='sport_list'),
    path('availableSchedule/<int:installation_id>/<str:date>', views.available_schedule, name='available_schedule'),
]