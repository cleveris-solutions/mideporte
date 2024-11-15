from rest_framework import generics
from .models import User
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        queryset = self.get_queryset()
        DNI = self.kwargs.get("DNI")
        return generics.get_object_or_404(queryset, DNI=DNI)