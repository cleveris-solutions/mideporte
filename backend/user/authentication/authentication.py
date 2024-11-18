from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import make_password
from ..models import User

class DNIAuthentication(BaseBackend):
    def authenticate(self,DNI=None):
        try:
            user = User.objects.get(DNI=DNI)
            return user
        except User.DoesNotExist:
            return None