from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes, api_view
from rest_framework import status
from api.permissions import IsAdminOrReadOnly
from django.contrib.auth.models import User
from rest_framework.viewsets import ModelViewSet
from .serializers import UserSerializer
from profiles.models import Profile
from profiles.serializers import ProfileSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAdminOrReadOnly,]

    
    def partial_update(self, request, pk=None):
        return Response({ "detail":  "This action is not authorized." }, status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, pk=None):
        user = self.get_object()
        profile = Profile.objects.filter(user_id=user.pk,)

        user_serializer = self.serializer_class(user, data=request.data,)
        profile_serializer = ProfileSerializer(profile, data=request.data,)

        if user_serializer.is_valid() and profile_serializer.is_valid():
            place = request.data['place']
            user_serializer.save()
            user.set_password(request.data['password'])
            user.save()
            profile.update(place=place, user=user)

            return Response(user_serializer.data)
        else:
            return Response(user_serializer.errors if profile_serializer.is_valid() else profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def create(self, request):
        user_serializer = self.serializer_class(data=request.data,)
        profile_serializer = ProfileSerializer(data=request.data,)

        if user_serializer.is_valid() and profile_serializer.is_valid():
            place = request.data['place']
            user = user_serializer.save()
            user.set_password(request.data['password'])
            user.save()
            Profile.objects.create(place=place, user=user)

            return Response(user_serializer.data)
        else:
            return Response(user_serializer.errors if profile_serializer.is_valid() else profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(methods=['get'], detail=False,)
    def user_info(self, request):
        user = request.user
        response = UserSerializer(user).data

        return Response(response) 


    @action(methods=['get'], detail=True,)
    def profile(self, request, pk=None):
        user = self.get_object()
        profile = Profile.objects.filter(user_id=user.pk,)
        response = ProfileSerializer(profile, many=True).data

        return Response(response) 

