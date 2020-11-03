from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from profiles.serializers import ProfileSerializer

class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email', 'is_superuser',]
        extra_kwargs = {'password': {'write_only': True},}


    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        # first_name = validated_data.pop('first_name')
        # last_name = validated_data.pop('last_name')
        # email = validated_data.pop('email')
        # is_superuser = validated_data.pop('is_superuser')

        user = User.objects.create_user(username=username, password=password,)
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
        user.is_superuser = validated_data.get('is_superuser', instance.is_superuser)
        user.set_password(password)
        user.save()
        
        return user


    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_auth_token(sender, instance=None, created=False, **kwargs):
        if created:
            Token.objects.create(user=instance)
