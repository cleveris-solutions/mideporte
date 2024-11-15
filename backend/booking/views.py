from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Booking
from user.models import User
from installation.models import Installation


@require_http_methods(["POST"])
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
        return JsonResponse({'error': 'User not found'}, status=404)
    except Installation.DoesNotExist:
        return JsonResponse({'error': 'Installation not found'}, status=404)

    return JsonResponse({'message': 'Booking created successfully', 'booking_id':booking.id}, status=201)
