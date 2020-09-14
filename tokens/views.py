from rest_framework.viewsets import ModelViewSet 
from .serializers import TokenSerializer 
from .models import Token


class TokenViewSet(ModelViewSet):
    queryset = Token.objects.all()
    serializer_class = TokenSerializer