from django.test import TestCase
from django.urls import reverse
from installation.models import Installation, InstallationType
from unittest.mock import patch
from datetime import date
from user.models import User 


class SportListTests(TestCase):
    fixtures = ['installation_initial_data.json', 'user_initial_data.json']
    
    def setUp(self):
        # Log in using the user from the fixture
        self.user = User.objects.get(DNI='12345678B')
        self.client.force_login(self.user)  

    def test_sport_list_success(self):
        # Make the request to the endpoint
        response = self.client.get(reverse('sport_list'))
        
        # Verify the status code
        self.assertEqual(response.status_code, 200)

        # Verify that the returned sports are unique
        sports = response.json()
        expected_sports = [
            {"id": 1, "name": "Piscina", "description": "Piscina municipal de verano", "image": "/media/installation_types/swim.png"},
            {"id": 2, "name": "Pádel", "description": "Pista de pádel cubierta", "image": "/media/installation_types/padel.png"},
            {"id": 3, "name": "Fútbol", "description": "Campo de fútbol de césped natural", "image": "/media/installation_types/football.png"},
            {"id": 4, "name": "Baloncesto", "description": "Pista de baloncesto al aire libre", "image": "/media/installation_types/basketball.png"}
        ]
        
        self.assertEqual(sports, expected_sports)

    def test_sport_list_no_installations(self):
        # Delete all installations and installation types
        Installation.objects.all().delete()
        InstallationType.objects.all().delete()

        # Make the request to the endpoint
        response = self.client.get(reverse('sport_list'))
        
        # Verify the status code
        self.assertEqual(response.status_code, 200)

        # Verify that the list is empty
        sports = response.json()
        self.assertEqual(sports, [])
        

class AvailableScheduleTests(TestCase):
    fixtures = ['installation_initial_data.json', 'user_initial_data.json']
    
    def setUp(self):
        # Log in using the user from the fixture
        self.user = User.objects.get(DNI='12345678B')
        self.client.force_login(self.user)  

    def test_available_schedule_success(self):
        installation = Installation.objects.first()
        installation_id = installation.pk
        target_date = date.today().strftime('%Y-%m-%d')

        with patch.object(Installation, 'get_available_hours', return_value=[
            MockAvailableHour(["09:00", "10:00"]),
            MockAvailableHour(["15:00", "16:00"]),
        ]):
            url = reverse('available_schedule', args=[installation_id, target_date])
            response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        expected_slots = ["09:00", "10:00", "15:00", "16:00"]
        self.assertEqual(response.json(), expected_slots)

    def test_available_schedule_installation_not_found(self):
        invalid_installation_id = 9999
        target_date = date.today().strftime('%Y-%m-%d')
        url = reverse('available_schedule', args=[invalid_installation_id, target_date])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"error": "Installation not found"})

    def test_available_schedule_invalid_date_format(self):
        installation = Installation.objects.first()
        installation_id = installation.pk
        invalid_date = "2024-13-40"
        url = reverse('available_schedule', args=[installation_id, invalid_date])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)

    def test_available_schedule_no_hours_available(self):
        installation = Installation.objects.first()
        installation_id = installation.pk
        target_date = date.today().strftime('%Y-%m-%d')

        with patch.object(Installation, 'get_available_hours', return_value=[]):
            url = reverse('available_schedule', args=[installation_id, target_date])
            response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

class MockAvailableHour:
    def __init__(self, hourly_slots):
        self.hourly_slots = hourly_slots

    def get_hourly_slots(self):
        return self.hourly_slots
