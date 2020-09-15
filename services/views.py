from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet 
from .serializers import ServiceSerializer 
from .models import Service


class ServiceViewSet(ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticated, IsAdminUser,]
