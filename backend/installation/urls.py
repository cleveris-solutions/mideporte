from django.urls import path
from . import views

urlpatterns = [
    path('sports', views.sport_list, name='sport_list'),
    path('schedule/<int:installation_id>/<str:date>', views.schedule, name='schedule'),
    path('availableSchedule/<int:installation_id>/<str:date>', views.available_schedule, name='available_schedule'),
    path('all', views.get_all_installations, name='get_all_installations'),
    path('type/<str:type>', views.get_installations_by_type, name='get_installations_by_type'),
]