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

    @action(methods=['get'], detail=False,)
    def user_info(self, request):
        user = request.user
        response = UserSerializer(user).data

        return Response(response) 


    def create(self, request):
        user_serializer = UserSerializer(data=request.data)

        if 'place' in request.data:
            place = request.data['place']
            if user_serializer.is_valid():
                user = user_serializer.save()
                Profile.objects.create(place=place, user=user)
                return Response(user_serializer.data)
            else:
                return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({ "place":  "This field is required." }, status=status.HTTP_400_BAD_REQUEST)


    @action(methods=['get'], detail=True,)
    def profile(self, request, pk=None):
        user = self.get_object()
        profile = Profile.objects.filter(user_id=user.pk,)
        response = ProfileSerializer(profile, many=True).data

        return Response(response) 
