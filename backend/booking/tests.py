from django.test import TestCase
from django.urls import reverse
from user.models import User
from installation.models import Installation
from booking.models import Booking, BookingStatus
from booking.serializers import BookingSerializer
from rest_framework.test import APIClient
from rest_framework import status
import json

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
        self.delete_booking = lambda booking_id: reverse('delete_booking', args=[booking_id])
        
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
            "installation": booking.installation.id,
            "start": "2024-11-19T10:00:00Z",
            "cancelled": False,
            "status": "Programada"
        })

    def test_create_booking_success(self):
        """Test successful booking creation."""
        payload = {
            "user_id": self.user.DNI,
            "installation_id": Installation.objects.first().id,
            "start_time": "2024-11-19T10:00:00Z"
        }
        response = self.client.post(self.create_booking_url, json.dumps(payload), content_type="application/json")

        # Check the response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn(MESSAGE, response.json())
        self.assertIn(BOOKING_ID, response.json())

        # Verify that the booking was created
        booking = Booking.objects.filter(user=self.user, installation_id=payload['installation_id'], start=payload['start_time'])
        self.assertTrue(booking.exists())

    def test_create_booking_user_not_found(self):
        """Test booking creation with a non-existent user."""
        payload = {
            "user_id": "77858824W",
            "installation_id": Installation.objects.first().id,
            "start_time": "2024-11-19T10:00:00Z",
        }
        response = self.client.post(self.create_booking_url, json.dumps(payload), content_type="application/json")

        # Check the response
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {"error": "User not found."})

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

    def test_cancel_booking_success(self):
        """Test successful booking cancellation."""
        booking = Booking.objects.filter(user=self.user).first()
        response = self.client.post(self.cancel_booking_url(booking.id))

        # Check the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {MESSAGE: SUCCESS_BOOKING_CANCELLED})

        # Verify that the booking status is Cancelled
        booking.refresh_from_db()
        self.assertEqual(booking.status, BookingStatus.Cancelled)

    def test_cancel_booking_not_found(self):
        """Test cancellation of a non-existent booking."""
        response = self.client.post(self.cancel_booking_url(9999))  # Non-existent booking ID

        # Check the response
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {ERROR: ERROR_BOOKING_NOT_FOUND})

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
        
    def test_delete_booking_success(self):
        """Test successful booking deletion."""
        booking = Booking.objects.create(
            user=self.user,
            installation=Installation.objects.first(),
            start="2024-11-19 10:00:00",
            status=BookingStatus.Scheduled
        )
        response = self.client.delete(self.delete_booking(booking.id))

        # Check the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {MESSAGE: SUCCESS_BOOKING_DELETED})

        # Verify that the booking was deleted
        self.assertFalse(Booking.objects.filter(id=booking.id).exists())
        
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
        
