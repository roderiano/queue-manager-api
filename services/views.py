from rest_framework.viewsets import ModelViewSet 
from .serializers import ServiceSerializer 
from .models import Service


class ServiceViewSet(ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer