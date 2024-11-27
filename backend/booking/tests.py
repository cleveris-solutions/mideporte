from django.test import TestCase
from django.urls import reverse
from user.models import User
from installation.models import Installation
from booking.models import Booking, BookingStatus
from booking.serializers import BookingSerializer
from rest_framework.test import APIClient
from rest_framework import status
import json
from unittest.mock import patch
from datetime import datetime, timedelta

BOOKING_ID = 'booking_id'
MESSAGE = 'message'         
ERROR = 'error'
ERROR_USER_NOT_FOUND = "User not found."
ERROR_INSTALLATION_NOT_FOUND = "Installation not found."
ERROR_BOOKING_NOT_FOUND = "Booking not found."
ERROR_MISSING_FIELD = "Missing field: {field}"
ERROR_INVALID_DATA = "Invalid data. Please check the request payload."
ERROR_CANCEL_BOOKING = "You can't cancel a booking one hour before the start time"
ERROR_NOT_ALLOWED_CANCEL_BOOKING = "You are not allowed to cancel this booking"
SUCCESS_BOOKING_CREATED = "Booking created successfully."
SUCCESS_BOOKING_CANCELLED = "Booking cancelled successfully."



class BookingTests(TestCase):
    fixtures = ['booking_initial_data.json', 'user_initial_data.json', 'installation_initial_data.json']

    def setUp(self):
        self.client = APIClient()

        # Get a user from the fixture
        self.user = User.objects.get(DNI='12345678B')
        self.client.force_login(user=self.user)  # Authenticate the user for the tests

        # URLs for the endpoints
        self.create_booking_url = reverse('create_booking') 
        self.cancel_booking_url = lambda booking_id: reverse('cancel_booking', args=[booking_id])  
        
    def test_get_scheduled_bookings(self):
        """Test getting all scheduled bookings."""
        response = self.client.get(reverse('get_scheduled_bookings'))
        bookings = Booking.objects.filter(status=BookingStatus.Scheduled)
        serializer = BookingSerializer(bookings, many=True)

        # Check the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            "bookings": serializer.data
        })
        
    def test_get_booking(self):
        """Test getting a single booking."""
        booking = Booking.objects.create(
            user=self.user,
            installation=Installation.objects.first(),
            start="2024-11-19 10:00:00",
            status=BookingStatus.Scheduled
        )
        response = self.client.get(reverse('get_booking', args=[booking.id]))

        # Check the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            "id": booking.id,
            "user": self.user.DNI,
            "installation": {
                "id": booking.installation.id,
                "name": booking.installation.name,
                "type": {
                    "id": booking.installation.type.id,
                    "name": booking.installation.type.name,
                    "description": booking.installation.type.description,
                    "image": booking.installation.type.image.url
                },
                "description": booking.installation.description,
                "availability": booking.installation.availability
            },
            "start": "2024-11-19T10:00:00Z",
            "status": "Programada"
        })

    @patch('booking.views.check_installation_disponibility', return_value=True)
    def test_create_booking_success(self, mock_check_installation_disponibility):
        """Test successful booking creation."""
        payload = {
            "installation_id": Installation.objects.first().id,
            "start_time": "2024-11-19T10:00:00Z"
        }
        response = self.client.post(self.create_booking_url, json.dumps(payload), content_type="application/json")

        # Check the response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('message', response.json())
        self.assertIn('booking_id', response.json())

        # Verify that the booking was created
        booking = Booking.objects.filter(user=self.user, installation_id=payload['installation_id'], start="2024-11-19 10:00:00")
        self.assertTrue(booking.exists())

    def test_create_booking_installation_not_found(self):
        """Test booking creation with a non-existent installation."""
        payload = {
            "user_id": self.user.DNI,
            "installation_id": 9999,  # Non-existent installation ID
            "start_time": "2024-11-19T10:00:00Z"
        }
        response = self.client.post(self.create_booking_url, json.dumps(payload), content_type="application/json")

        # Check the response
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {ERROR: ERROR_INSTALLATION_NOT_FOUND})
        
    def test_create_booking_invalid_payload(self):
        """Test booking creation with invalid payload."""
        payload = {
            "user_id": self.user.DNI,
            # Missing installation_id field
            "start_time": "2024-11-19T10:00:00Z",
            
        }
        response = self.client.post(self.create_booking_url, json.dumps(payload), content_type="application/json")

        # Check the response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {ERROR: ERROR_MISSING_FIELD.format(field='installation_id')})

    @patch('booking.views.check_installation_disponibility', return_value=True)
    def test_create_booking_more_than_two_bookings_same_time(self, mock_check_installation_disponibility):
        """Test creating a booking when the user already has two bookings at the same time."""
        installation = Installation.objects.first()
        start_time = datetime.now() + timedelta(days=1)
        Booking.objects.create(user=self.user, installation=installation, start=start_time, status=BookingStatus.Scheduled)

        payload = {
            "installation_id": installation.id,
            "start_time": start_time.strftime('%Y-%m-%dT%H:%M:%SZ')
        }
        response1 = self.client.post(self.create_booking_url, json.dumps(payload), content_type="application/json")
        response2 = self.client.post(self.create_booking_url, json.dumps(payload), content_type="application/json")

        # Check the response
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response2.json(), {"error": "You can't have more than two bookings at the same time"})

    @patch('booking.views.check_installation_disponibility', return_value=True)
    def test_create_booking_more_than_two_consecutive_bookings_same_installation(self, mock_check_installation_disponibility):
        """Test creating a booking when the user already has two consecutive bookings at the same installation."""
        installation = Installation.objects.first()
        start_time = datetime.now() + timedelta(days=1)
        Booking.objects.create(user=self.user, installation=installation, start=start_time - timedelta(hours=1), status=BookingStatus.Scheduled)
        Booking.objects.create(user=self.user, installation=installation, start=start_time + timedelta(hours=1), status=BookingStatus.Scheduled)

        payload = {
            "installation_id": installation.id,
            "start_time": start_time.strftime('%Y-%m-%dT%H:%M:%SZ')
        }
        response = self.client.post(self.create_booking_url, json.dumps(payload), content_type="application/json")

        # Check the response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {"error": "You can't have more than two consecutive bookings at the same installation"})

    def test_cancel_booking_success(self):
        """Test successful booking cancellation."""
        future_time = datetime.now() + timedelta(hours=2)
        booking = Booking.objects.create(
            user=self.user,
            installation=Installation.objects.first(),
            start=future_time + timedelta(hours=1),
            status=BookingStatus.Scheduled
        )
        response = self.client.post(self.cancel_booking_url(booking.id))

        # Check the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {MESSAGE: SUCCESS_BOOKING_CANCELLED})

        # Verify that the booking status is Cancelled
        booking.refresh_from_db()
        self.assertEqual(booking.status, BookingStatus.Cancelled)

    def test_cancel_booking_one_hour_before_start_time(self):
        """Test cancellation of a booking one hour before the start time."""
        booking = Booking.objects.filter(user=self.user).first()
        response = self.client.post(self.cancel_booking_url(booking.id))

        # Check the response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {ERROR: ERROR_CANCEL_BOOKING})

        # Verify that the booking status is NOT Cancelled
        booking.refresh_from_db()
        self.assertNotEqual(booking.status, BookingStatus.Cancelled)
        
    def test_cancel_booking_not_allowed(self):
        """Test cancellation of a booking by a user who is not the owner."""
        booking = Booking.objects.exclude(user=self.user).first()
        response = self.client.post(self.cancel_booking_url(booking.id))

        # Check the response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {ERROR: ERROR_NOT_ALLOWED_CANCEL_BOOKING})

        # Verify that the booking status is NOT Cancelled
        booking.refresh_from_db()
        self.assertNotEqual(booking.status, BookingStatus.Cancelled)

    def test_cancel_booking_not_found(self):
        """Test cancellation of a non-existent booking."""
        response = self.client.post(self.cancel_booking_url(9999))  # Non-existent booking ID

        # Check the response
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {ERROR: ERROR_BOOKING_NOT_FOUND})
        
    def test_bookings_by_user_success(self):
        """Test getting all bookings of a user."""
        response = self.client.get(reverse('get_bookings_by_user', args=[self.user.DNI]))
        bookings = Booking.objects.filter(user=self.user)
        serializer = BookingSerializer(bookings, many=True)

        # Check the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            "bookings": serializer.data
        })
        
