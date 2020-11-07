from .models import Token
from departments.serializers import DepartmentSerializer
from services.serializers import ServiceSerializer
from rest_framework.serializers import ModelSerializer 


class TokenSerializer(ModelSerializer):

    class Meta:
        model = Token
        fields = ['id', 'key', 'department', 'status', 'issue_date', 'attendence_date', 'archived_date', 'time_waiting_attendence', 'time_in_attendence', 'service', 'clerk', 'token_type',]
        extra_kwargs = {'status': {'read_only': True}, 
                        'key': {'read_only': True}, 
                        'issue_date': {'read_only': True}, 
                        'attendence_date': {'read_only': True},
                        'archived_date': {'read_only': True},
                        'time_waiting_attendence': {'read_only': True},
                        'time_in_attendence': {'read_only': True},
                        'service': {'read_only': True},
                        'clerk': {'read_only': True},
                        }

