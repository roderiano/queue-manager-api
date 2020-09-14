from .models import Department
from services.serializers import ServiceSerializer
from rest_framework.serializers import ModelSerializer 

class DepartmentSerializer(ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name',]