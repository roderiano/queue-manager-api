from .models import Department
from rest_framework.serializers import ModelSerializer 


class DepartmentSerializer(ModelSerializer):

    class Meta:
        model = Department
        fields = ['id', 'name', 'code', 'available_services',]
        extra_kwargs = {'available_services': {'write_only': True}}