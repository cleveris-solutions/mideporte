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
                return Response({'error': 'Se requiere DNI para autenticación'}, status=status.HTTP_400_BAD_REQUEST)

        user = DNIAuthentication.authenticate(self,DNI=dni)
        if user is None:
            return Response({'error': 'DNI no registrado'}, status=status.HTTP_401_UNAUTHORIZED)

        if user.suspended:
            return Response({'error': 'Cuenta suspendida'}, status=status.HTTP_403_FORBIDDEN)
        
        
        token,_ = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'user':{
                'DNI': user.DNI,
                'suspended': user.suspended,
                'is_staff': user.is_staff
            }
        })