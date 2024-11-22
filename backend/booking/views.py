from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Booking, BookingStatus
from user.models import User
from .serializers import BookingSerializer
from installation.models import Installation
from rest_framework.decorators import api_view
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

BOOKINGS = "bookings"
BOOKING_ID = 'booking_id'
MESSAGE = 'message'         
ERROR = 'error'
ERROR_USER_NOT_FOUND = "User not found."
ERROR_INSTALLATION_NOT_FOUND = "Installation not found."
ERROR_BOOKING_NOT_FOUND = "Booking not found."
ERROR_MISSING_FIELD = "Missing field: {field}"
ERROR_INVALID_DATA = "Invalid data. Please check the request payload."
SUCCESS_BOOKING_CREATED = "Booking created successfully."
SUCCESS_BOOKING_CANCELLED = "Booking cancelled successfully."
SUCCESS_BOOKING_DELETED = "Booking deleted successfully."
SUCCESS_BOOKING_UPDATED = "Booking updated successfully."

@extend_schema()
@require_http_methods(["GET"])
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_scheduled_bookings(request):
    bookings = Booking.objects.filter(status=BookingStatus.Scheduled)
    serializer = BookingSerializer(bookings, many=True)
    return JsonResponse({BOOKINGS: serializer.data}, status=200)

@extend_schema()
@require_http_methods(["GET"])
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_booking(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id)
        serializer = BookingSerializer(booking)
    except Booking.DoesNotExist:
        return JsonResponse({ERROR: ERROR_BOOKING_NOT_FOUND}, status=404)

    return JsonResponse(serializer.data, status=200, safe=False)

@extend_schema()
@require_http_methods(["GET"])
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_bookings_by_user(request, dni):
    try:
        user = User.objects.get(DNI=dni)
        bookings = Booking.objects.filter(user=user)
        serializer = BookingSerializer(bookings, many=True)
    except User.DoesNotExist:
        return JsonResponse({ERROR: ERROR_USER_NOT_FOUND}, status=404)

    return JsonResponse({BOOKINGS: serializer.data}, status=200)
    

@extend_schema()
@require_http_methods(["POST"])
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_booking(request):
    data = json.loads(request.body)
    required_fields = ['user_id', 'installation_id', 'start_time']
    for field in required_fields:
        if field not in data:
            return JsonResponse({ERROR: ERROR_MISSING_FIELD.format(field=field)}, status=400)

    user_dni = data['user_id']
    installation = data['installation_id']
    start_time = data['start_time']
    try:
        user = User.objects.get(DNI=user_dni)
        installation = Installation.objects.get(id=installation)
        booking = Booking.objects.create(user=user,
                                         installation=installation, 
                                         start=start_time,
                                         status=BookingStatus.Scheduled)
    except User.DoesNotExist:
        return JsonResponse({ERROR: ERROR_USER_NOT_FOUND}, status=404)
    except Installation.DoesNotExist:
        return JsonResponse({ERROR: ERROR_INSTALLATION_NOT_FOUND}, status=404)

    return JsonResponse({MESSAGE: SUCCESS_BOOKING_CREATED, BOOKING_ID:booking.id}, status=201)


#* Method to cancel a booking by changing its status to cancelled
@extend_schema()
@require_http_methods(["POST"])     
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def cancel_booking(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id)
        booking.status = BookingStatus.Cancelled
        booking.save()
    except Booking.DoesNotExist:
        return JsonResponse({ERROR: ERROR_BOOKING_NOT_FOUND}, status=404)

    return JsonResponse({MESSAGE: SUCCESS_BOOKING_CANCELLED}, status=200)


@extend_schema()
@require_http_methods(["DELETE"])
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_booking(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id)
        booking.delete()
    except Booking.DoesNotExist:
        return JsonResponse({ERROR: ERROR_BOOKING_NOT_FOUND}, status=404)

    return JsonResponse({MESSAGE: SUCCESS_BOOKING_DELETED}, status=200)