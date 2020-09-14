from .models import Service
from rest_framework.serializers import ModelSerializer 

class ServiceSerializer(ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name']