from rest_framework import serializers
from .models import Booking

class BookingSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.DNI')
    class Meta:
        model = Booking
        fields = '__all__'