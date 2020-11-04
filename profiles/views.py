from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes, api_view
from api.permissions import IsAdminOrReadOnly
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from .models import Profile
from .serializers import ProfileSerializer


class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAdminOrReadOnly,]

    def create(self, request):
        return Response({ "detail":  "This action is not authorized." }, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        return Response({ "detail":  "This action is not authorized." }, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        return Response({ "detail":  "This action is not authorized." }, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        return Response({ "detail":  "This action is not authorized." }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        return Response({ "detail":  "This action is not authorized." }, status=status.HTTP_400_BAD_REQUEST)