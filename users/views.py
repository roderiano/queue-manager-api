from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes, api_view
from api.permissions import IsAdminOrReadOnly
from django.contrib.auth.models import User
from rest_framework.viewsets import ModelViewSet
from .serializers import UserSerializer


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

