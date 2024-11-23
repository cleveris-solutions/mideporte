from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Installation, InstallationType
from datetime import datetime
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, api_view
from .serializers import InstallationTypeSerializer, InstallationSerializer
from django.shortcuts import get_object_or_404


INSTALLATION_NOT_FOUND_MSG = 'Installation not found'
ERROR_KEY = 'error'
INVALID_DATE_FORMAT_MSG = 'Invalid date format'


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

    return JsonResponse(available_hours, safe=False)



