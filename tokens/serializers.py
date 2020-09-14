from .models import Token
from rest_framework.serializers import ModelSerializer 

class TokenSerializer(ModelSerializer):
    class Meta:
        model = Token
        fields = ['id', 'status', 'departament', 'issue_date', 'attendence_date', 'archived_date', 'service', 'clerk']