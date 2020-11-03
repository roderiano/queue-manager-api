from .models import Profile
from rest_framework.serializers import ModelSerializer 

class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = ['place',]