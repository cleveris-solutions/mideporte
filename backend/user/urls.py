from django.urls import path
from .views import UserDetail
from .views import AuthenticateDNI

urlpatterns = [
    path('<str:DNI>', UserDetail.as_view(), name='user-detail'),
    path('authenticate/',AuthenticateDNI.as_view(),name = 'authenticate-user')
]