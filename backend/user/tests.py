from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from user.models import User
from rest_framework.authtoken.models import Token

ERROR = 'error'
DNI_REQUIRED_MESSAGE = 'Se requiere DNI para autenticación'
DNI_UNREGISTERED_MESSAGE = 'DNI no registrado'
USER_SUSPENDED_MESSAGE = 'Cuenta suspendida'
DNI = 'DNI'

class UserDetailTests(TestCase):
    fixtures = ['user_initial_data.json']

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.get(DNI='12345678B')
        self.user_url = reverse('user-detail', args=['12345678B'])
        self.token = Token.objects.create(user=self.user)

        
    def test_user_detail_unauthenticated(self):
        """Test user detail without authentication."""
        response = self.client.get(self.user_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_user_detail_authenticated(self):
        """Test user detail with authentication."""
        user = User.objects.get(DNI='12345678B')
        token = Token.objects.get(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get(self.user_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            'DNI': user.DNI,
            'suspended': user.suspended,
            'is_staff': user.is_staff,
            'name': user.name,
            'surname': user.surname,
            'email': user.email,
            'telephone_number': user.telephone_number
        })

class AuthenticationTests(TestCase):
    fixtures = ['user_initial_data.json']

    def setUp(self):
        self.client = APIClient()
        self.authenticate_url = reverse('authenticate-user')

    def test_authenticate_missing_dni(self):
        """Test authentication with missing DNI."""
        response = self.client.post(self.authenticate_url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {ERROR: DNI_REQUIRED_MESSAGE})

    def test_authenticate_unregistered_dni(self):
        """Test authentication with unregistered DNI."""
        response = self.client.post(self.authenticate_url, {DNI: '99999999Z'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json(), {ERROR: DNI_UNREGISTERED_MESSAGE})

    def test_authenticate_suspended_account(self):
        """Test authentication with suspended account."""
        user = User.objects.get(DNI='12345678B')
        user.suspended = True
        user.save()
        response = self.client.post(self.authenticate_url, {DNI: user.DNI})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), {ERROR: USER_SUSPENDED_MESSAGE})

    def test_authenticate_success(self):
        """Test successful authentication."""
        user = User.objects.get(DNI='12345678B')
        response = self.client.post(self.authenticate_url, {DNI: user.DNI})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = Token.objects.get(user=user)
        self.assertEqual(response.json(), {
            'token': token.key,
            'user': {
                'DNI': user.DNI,
                'suspended': user.suspended,
                'is_staff': user.is_staff,
                'name': user.name,
                'surname': user.surname,
                'email': user.email,
                'telephone_number': user.telephone_number
            }
        })