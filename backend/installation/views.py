from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Installation, InstallationType
from datetime import datetime
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, api_view
from .serializers import InstallationTypeSerializer, InstallationSerializer
from django.shortcuts import get_object_or_404
from booking.models import Booking, BookingStatus


INSTALLATION_NOT_FOUND_MSG = 'Instalación no encontrada'
ERROR_KEY = 'error'
INVALID_DATE_FORMAT_MSG = 'Formato de fecha inválido'


@require_http_methods(["GET"])
@permission_classes([IsAuthenticated])
@api_view(["GET"])
def get_all_installations(request):
    installations = Installation.objects.all()
    serializer = InstallationSerializer(installations, many=True)
    return JsonResponse(serializer.data, safe=False, json_dumps_params={'indent': 4, 'ensure_ascii': False})


@require_http_methods(["GET"])
@permission_classes([IsAuthenticated])
@api_view(["GET"])
def get_installations_by_type(request, type):
    installation_type = get_object_or_404(InstallationType, name=type)
    installations = Installation.objects.filter(type=installation_type)
    installations_data = InstallationSerializer(installations, many=True)
    return JsonResponse(installations_data.data, safe=False, json_dumps_params={'indent': 4, 'ensure_ascii': False})


@require_http_methods(["GET"])
@permission_classes([IsAuthenticated])
@api_view(["GET"])
def sport_list(request):
    sports = InstallationType.objects.all()
    serializer = InstallationTypeSerializer(sports, many=True)
    return JsonResponse(serializer.data, safe=False, json_dumps_params={'indent': 4})


@require_http_methods(["GET"])
@api_view(["GET"])
def schedule(request, installation_id, date):
    try:
        installation = Installation.objects.get(pk=installation_id)
    except Installation.DoesNotExist:
        return JsonResponse({ERROR_KEY: INSTALLATION_NOT_FOUND_MSG}, status=404)

    try:
        date = datetime.strptime(date, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({ERROR_KEY: INVALID_DATE_FORMAT_MSG}, status=400)
    
    available_hours = installation.get_open_hours(date)

    return JsonResponse(available_hours, safe=False)


@require_http_methods(["GET"])
@api_view(["GET"])
def available_schedule(request, installation_id, date):
    try:
        installation = Installation.objects.get(pk=installation_id)
    except Installation.DoesNotExist:
        return JsonResponse({ERROR_KEY: INSTALLATION_NOT_FOUND_MSG}, status=404)

    try:
        date = datetime.strptime(date, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({ERROR_KEY: INVALID_DATE_FORMAT_MSG}, status=400)
    
    current_date = datetime.now()
    # current_date = localtime(current_date)
    
    if date >= current_date.date():
        open_hours = installation.get_open_hours(date)
        booked_hours = Booking.objects.filter(installation=installation, start__date=date, status=BookingStatus.Scheduled).values_list('start', flat=True)
        booked_hours = [hour.strftime('%H:%M') for hour in booked_hours]
        
        current_time = current_date.time()
        available_hours = [hour for hour in open_hours if hour not in booked_hours and datetime.strptime(hour, '%H:%M').time() >= current_time]
        
        return JsonResponse(available_hours, safe=False)
    else:
        return JsonResponse([], safe=False)



