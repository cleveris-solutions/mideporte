from django.urls import path
from .views import UserDetail

urlpatterns = [
    path('users/<str:DNI>/', UserDetail.as_view(), name='user-detail'),
]