from django.contrib import admin
from django.urls import include, path
from installation import views as installation_views
from booking import views as booking_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/sports', installation_views.sport_list, name='sport_list'),
    path('api/v1/bookings', booking_views.create_booking, name='create_booking'),
    path('api/v1/availableSchedule/<int:installation_id>/<str:date>', installation_views.available_schedule, name='available_schedule'),
]
