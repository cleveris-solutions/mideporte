from rest_framework import serializers
from .models import InstallationType, Installation

class InstallationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstallationType
        fields = ['id', 'name', 'description', 'image']
        
        
class InstallationSerializer(serializers.ModelSerializer):
    type = InstallationTypeSerializer()
    class Meta:
        model = Installation
        fields = ['id', 'name', 'type', 'description', 'availability']