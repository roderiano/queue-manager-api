from rest_framework.viewsets import ModelViewSet 
from .serializers import DepartmentSerializer 
from .models import Department


class DepartmentViewSet(ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer