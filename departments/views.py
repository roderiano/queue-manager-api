from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from services.models import Service 
from services.serializers import ServiceSerializer
from .serializers import DepartmentSerializer
from .models import Department


class DepartmentViewSet(ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    # Method to list all availabe services at departmet
    @action(methods=['get'], detail=True,)
    def available_services(self, request, pk=None):
        department = self.get_object()
        serializer = ServiceSerializer(department.available_services.all(), many=True)

        return Response(serializer.data) 