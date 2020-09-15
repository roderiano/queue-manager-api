from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    
    def update(self, instance, validated_data):
        password = validated_data.pop('password')
        user = instance
        user.username = validated_data.get('username', instance.username)
        user.first_name = validated_data.get('first_name', instance.first_name)
        user.last_name = validated_data.get('last_name', instance.last_name)
        user.email = validated_data.get('email', instance.email)
        user.set_password(password)
        user.save()
        return user
