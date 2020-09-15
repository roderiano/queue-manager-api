from rest_framework.viewsets import ModelViewSet 
from rest_framework.decorators import action
from rest_framework.response import Response
from departments.serializers import DepartmentSerializer
from services.serializers import ServiceSerializer
from users.serializers import UserSerializer
from .serializers import TokenSerializer 
from .models import Token
from .exceptions import *
from django.utils import timezone
import datetime as dt


class TokenViewSet(ModelViewSet):
    queryset = Token.objects.all()
    serializer_class = TokenSerializer


    @action(methods=['get'], detail=True,)
    def start_attendence(self, request, pk=None):
        token = self.get_object()
        current_user = request.user

        if token.status == 'TIS':
            token.status = 'IAT'
            token.attendence_date = dt.datetime.now(tz=timezone.utc) 
            token.time_waiting_attendence = token.attendence_date - token.issue_date
            token.clerk = current_user
            token.save()
            response = TokenSerializer(token).data 
        elif token.status == 'IAT':
            raise AttendenceAlreadyStartedException()
        elif token.status == 'TAR':
            raise TokenAlreadyArchivedException() 

        return Response(response) 


    @action(methods=['get'], detail=True,)
    def archive_token(self, request, pk=None):
        token = self.get_object()
        if token.status == 'IAT':
            token.status = 'TAR'
            token.archived_date = dt.datetime.now(tz=timezone.utc) 
            token.time_in_attendence = token.archived_date - token.attendence_date
            token.save()
            response = TokenSerializer(token).data 
        elif token.status == 'TIS':
            raise AttendenceNotStartedException()
        elif token.status == 'TAR':
            raise TokenAlreadyArchivedException() 

        return Response(response) 


    @action(methods=['get'], detail=True,)
    def service(self, request, pk=None):
        token = self.get_object()

        if token.status == 'TAR':
            response = ServiceSerializer(token.service).data 
        else:
            raise TokenNotArchivedException()

        return Response(response) 

    @action(methods=['get'], detail=True,)
    def department(self, request, pk=None):
        token = self.get_object()
        response = DepartmentSerializer(token.department).data 

        return Response(response) 


    @action(methods=['get'], detail=True,)
    def clerk(self, request, pk=None):
        token = self.get_object()
        response = UserSerializer(token.clerk).data 

        return Response(response) 

