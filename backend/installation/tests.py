from django.test import TestCase
from django.urls import reverse
from .models import Installation, InstallationType

class SportListTests(TestCase):

    def setUp(self):
        # Create test data: installations with associated sports
        Installation.objects.create(name="Piscina Municipal", type=InstallationType.SWIMMING_POOL, availability=True)
        Installation.objects.create(name="Pista de Pádel 1", type=InstallationType.PADEL, availability=True)
        Installation.objects.create(name="Campo de Fútbol", type=InstallationType.FOOTBALL, availability=True)
        Installation.objects.create(name="Pista de Baloncesto", type=InstallationType.BASKETBALL, availability=False)
        
    def test_sport_list_success(self):
        # Make the request to the endpoint
        response = self.client.get(reverse('sport_list'))
        
        # Verify the status code
        self.assertEqual(response.status_code, 200)

        # Verify that the returned sports are unique
        sports = response.json()
        self.assertCountEqual(sports, [
            InstallationType.SWIMMING_POOL,
            InstallationType.PADEL,
            InstallationType.FOOTBALL,
            InstallationType.BASKETBALL
        ])

    def test_sport_list_no_installations(self):
        # Delete all installations
        Installation.objects.all().delete()

        # Make the request to the endpoint
        response = self.client.get(reverse('sport_list'))
        
        # Verify the status code
        self.assertEqual(response.status_code, 200)

        # Verify that the list is empty
        sports = response.json()
        self.assertEqual(sports, [])