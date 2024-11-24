from rest_framework import serializers
from .models import Booking
from installation.serializers import InstallationSerializer

class BookingSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.DNI')
    installation = InstallationSerializer()
    
    class Meta:
        model = Booking
        fields = '__all__'