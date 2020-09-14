from .models import Token
from departments.serializers import DepartmentSerializer
from services.serializers import ServiceSerializer
from rest_framework.serializers import ModelSerializer 


class TokenSerializer(ModelSerializer):
    class Meta:
        model = Token
        fields = ['id', 'status', 'department', 'issue_date', 'attendence_date', 'archived_date', 'time_in_attendence', 'time_waiting_attendence', 'service', 'clerk']