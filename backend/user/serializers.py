from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['DNI','name','surname','email','telephone_number','suspended', 'is_staff']