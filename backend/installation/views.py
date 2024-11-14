from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Installation


@require_http_methods(["GET"])
def sport_list(request):
    sports = Installation.objects.values_list('type', flat=True).distinct()
    return JsonResponse(list(sports), safe=False)



