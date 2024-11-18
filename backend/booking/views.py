from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Booking, BookingStatus
from user.models import User
from installation.models import Installation
from rest_framework.decorators import api_view
from drf_spectacular.utils import extend_schema,OpenApiParameter,OpenApiExample,OpenApiTypes
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

MESSAGE = 'message'         
ERROR = 'error'
ERROR_USER_NOT_FOUND = "User not found."
ERROR_INSTALLATION_NOT_FOUND = "Installation not found."
ERROR_BOOKING_NOT_FOUND = "Booking not found."
ERROR_INVALID_DATA = "Invalid data. Please check the request payload."
SUCCESS_BOOKING_CREATED = "Booking created successfully."
SUCCESS_BOOKING_CANCELLED = "Booking cancelled successfully."

@extend_schema()
@require_http_methods(["POST"])
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_booking(request):
    data = json.loads(request.body)
    user = data['user_id']
    installation = data['installation_id']
    date = data['date']
    start_time = data['start_time']
    end_time = data['end_time']
    try:
        user = User.objects.get(id=user)
        installation = Installation.objects.get(id=installation)
        booking = Booking.objects.create(user=user,
                                         installation=installation, 
                                         date=date,
                                         start_time=start_time,
                                         end_time=end_time)
    except User.DoesNotExist:
        return JsonResponse({ERROR: ERROR_USER_NOT_FOUND}, status=404)
    except Installation.DoesNotExist:
        return JsonResponse({ERROR: ERROR_INSTALLATION_NOT_FOUND}, status=404)

    return JsonResponse({ERROR: SUCCESS_BOOKING_CREATED, 'booking_id':booking.id}, status=201)


#* Method to cancel a booking by changing its status to cancelled
@extend_schema()
@require_http_methods(["POST"])     
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def cancel_booking(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id)
        booking.status = BookingStatus.CANCELLED
        booking.save()
    except Booking.DoesNotExist:
        return JsonResponse({ERROR: ERROR_BOOKING_NOT_FOUND}, status=404)

    return JsonResponse({MESSAGE: SUCCESS_BOOKING_CANCELLED}, status=200)