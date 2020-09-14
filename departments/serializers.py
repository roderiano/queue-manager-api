from .models import Department
from rest_framework.serializers import ModelSerializer 

class DepartmentSerializer(ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'services']