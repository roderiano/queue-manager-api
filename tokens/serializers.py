from .models import Token
from departments.serializers import DepartmentSerializer
from services.serializers import ServiceSerializer
from rest_framework.serializers import ModelSerializer 


class TokenSerializer(ModelSerializer):

    class Meta:
        model = Token
        fields = ['id', 'department', 'status',]
        extra_kwargs = {'status': {'read_only': True}}



