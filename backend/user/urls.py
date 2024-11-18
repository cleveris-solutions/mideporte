from django.urls import path
from .views import UserDetail

urlpatterns = [
    path('<str:DNI>', UserDetail.as_view(), name='user-detail'),
]