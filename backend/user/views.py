from rest_framework import generics
from .models import User
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .authentication.authentication import DNIAuthentication


ERROR = 'error'
DNI_REQUIRED_MESSAGE = 'Se requiere DNI para autenticación'
DNI_UNREGISTERED_MESSAGE = 'DNI no registrado'
USER_SUSPENDED_MESSAGE = 'Cuenta suspendida'


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        queryset = self.get_queryset()
        DNI = self.kwargs.get("DNI")
        return generics.get_object_or_404(queryset, DNI=DNI)
    
class AuthenticateDNI(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        dni = request.data.get('DNI','').strip()
        
        if not dni:
                return Response({ERROR: DNI_REQUIRED_MESSAGE}, status=status.HTTP_400_BAD_REQUEST)

        user = DNIAuthentication.authenticate(self,DNI=dni)
        if user is None:
            return Response({ERROR: DNI_UNREGISTERED_MESSAGE}, status=status.HTTP_401_UNAUTHORIZED)

        if user.suspended:
            return Response({ERROR: USER_SUSPENDED_MESSAGE}, status=status.HTTP_403_FORBIDDEN)
        
        
        token,_ = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'user':{
                'DNI': user.DNI,
                'suspended': user.suspended,
                'is_staff': user.is_staff,
                'name': user.name,
                'surname': user.surname,
                'email': user.email,
                'telephone_number': user.telephone_number
            }
        })