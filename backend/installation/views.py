from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Installation
from datetime import datetime
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes


INSTALLATION_NOT_FOUND_MSG = 'Installation not found'
ERROR_KEY = 'error'
INVALID_DATE_FORMAT_MSG = 'Invalid date format'

@require_http_methods(["GET"])
@permission_classes([IsAuthenticated])
def sport_list(request):
    sports = Installation.objects.values_list('type', flat=True).distinct()
    return JsonResponse(list(sports), safe=False)

@require_http_methods(["GET"])
def available_schedule(request, installation_id, date):
    try:
        installation = Installation.objects.get(pk=installation_id)
    except Installation.DoesNotExist:
        return JsonResponse({ERROR_KEY: INSTALLATION_NOT_FOUND_MSG}, status=404)

    try:
        date = datetime.strptime(date, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({ERROR_KEY: INVALID_DATE_FORMAT_MSG}, status=400)
    
    available_hours = installation.get_available_hours(date)
    
    hourly_slots = []
    for available_hour in available_hours:
        hourly_slots.extend(available_hour.get_hourly_slots())

    return JsonResponse(hourly_slots, safe=False)



