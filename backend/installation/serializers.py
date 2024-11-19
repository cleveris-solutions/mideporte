from rest_framework import serializers
from .models import InstallationType

class InstallationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstallationType
        fields = ['id', 'name', 'description', 'image']