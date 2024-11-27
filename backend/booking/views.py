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
from datetime import datetime, timedelta
from django.utils import timezone

BOOKINGS = "bookings"
BOOKING_ID = 'booking_id'
MESSAGE = 'message'         
ERROR = 'error'
ERROR_USER_NOT_FOUND = "Usuario no encontrado."
ERROR_INSTALLATION_NOT_FOUND = "Instalación no encontrada."
ERROR_BOOKING_NOT_FOUND = "Reserva no encontrada."
ERROR_MISSING_FIELD = "Falta el campo: {field}"
ERROR_INVALID_DATA = "Datos inválidos. Por favor, revise los campos."
SUCCESS_BOOKING_CREATED = "Instalación reservada con éxito."
SUCCESS_BOOKING_CANCELLED = "Reserva cancelada con éxito."
INVALID_DATE_FORMAT_MSG = "Formato de fecha inválido. Por favor, use el formato: YYYY-MM-DDTHH:MM:SSZ"

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
    

def check_installation_disponibility(installation, date):
    availibility = True
    hour = date.strftime('%H:%M')
    # Check if the date is among the installation open hours
    available_hours = installation.get_open_hours(date.date()) 
    if hour not in available_hours:
        availibility = False
            
    # Check if there is already a booking for that date and hour
    bookings = Booking.objects.filter(installation=installation, start=date).exclude(status=BookingStatus.Cancelled)
    if bookings:
        availibility = False
        
    if not availibility:
        raise Exception("La instalación no está disponible en la fecha y hora seleccionadas")
    
def user_booking_viability(user, installation, date):
    # Check if the user has already a booking for other installation at the same date and time
    bookings_same_time = Booking.objects.filter(user=user, start=date).exclude(status=BookingStatus.Cancelled)
    if bookings_same_time:
        raise Exception("No puedes tener más de una reserva a la misma hora")

    # Check if the user has already two consecutive bookings at the same installation
    start_range = date - timedelta(hours=2)
    end_range = date + timedelta(hours=2)

    bookings_same_installation = Booking.objects.filter(user=user, 
                                                        installation=installation,
                                                        start__range=(start_range, end_range)
                                                        ).exclude(status=BookingStatus.Cancelled)
    if len(bookings_same_installation) >= 2:
        raise Exception("No puedes tener más de dos reservas consecutivas en la misma instalación")

@extend_schema()
@require_http_methods(["POST"])
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_booking(request):
    data = json.loads(request.body)
    required_fields = ['installation_id', 'start_time']
    for field in required_fields:
        if field not in data:
            return JsonResponse({ERROR: ERROR_MISSING_FIELD.format(field=field)}, status=400)

    user = request.user
    if user.suspended:
        raise Exception("No puedes reservar una pista porque tu cuenta está suspendida")
    installation_id = data['installation_id']
    start_time = data['start_time']
    try:
        installation = Installation.objects.get(id=installation_id)
        date = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%SZ').replace(minute=0, second=0, microsecond=0)
        # Check if the user can book the installation at the selected date and time
        check_installation_disponibility(installation, date)
        user_booking_viability(user, installation, date)
        booking = Booking.objects.create(user=user,
                                         installation=installation, 
                                         start=date,
                                         status=BookingStatus.Scheduled)
    except Installation.DoesNotExist:
        return JsonResponse({ERROR: ERROR_INSTALLATION_NOT_FOUND}, status=404)
    except ValueError:
        return JsonResponse({ERROR: INVALID_DATE_FORMAT_MSG}, status=400)
    except Exception as e:
        return JsonResponse({ERROR: str(e)}, status=400)

    return JsonResponse({MESSAGE: SUCCESS_BOOKING_CREATED, BOOKING_ID:booking.id}, status=201)


#* Method to cancel a booking by changing its status to cancelled
@extend_schema()
@require_http_methods(["POST"])     
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def cancel_booking(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id)
        
        # Check user ownership
        if booking.user != request.user:
            raise Exception("No puedes cancelar esta reserva porque no eres el propietario.")
        
        # Check if the booking is not set one hour after the cancellation
        if booking.start - timedelta(hours=1) < timezone.now():
            raise Exception("No puedes cancelar la reserva una hora antes de la hora de inicio.")

        booking.status = BookingStatus.Cancelled
        booking.save()
    except Booking.DoesNotExist:
        return JsonResponse({ERROR: ERROR_BOOKING_NOT_FOUND}, status=404)
    except Exception as e:
        return JsonResponse({ERROR: str(e)}, status=400)

    return JsonResponse({MESSAGE: SUCCESS_BOOKING_CANCELLED}, status=200)
