from rest_framework.authentication import TokenAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet 
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import MethodNotAllowed 
from departments.serializers import DepartmentSerializer
from services.serializers import ServiceSerializer
from services.models import Service
from users.serializers import UserSerializer
from .serializers import TokenSerializer 
from .models import Token
from .exceptions import *
from django.utils import timezone
import datetime as dt
from rest_framework import status
from departments.models import Department


class TokenViewSet(ModelViewSet):
    queryset = Token.objects.all()
    serializer_class = TokenSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter,]
    
    fields = ['id', 'key', 'status', 'department', 'issue_date', 'attendence_date', 'archived_date',
                        'time_waiting_attendence', 'time_in_attendence', 'service', 'clerk', 'token_type',]
    ordering_fields = fields
    filterset_fields = fields

    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticated,]


    def create(self, request):
        token_serializer = TokenSerializer(data=request.data)
        if token_serializer.is_valid():
            department = Department.objects.get(pk=request.data['department']) 
            daily_tokens = Token.objects.filter(issue_date__year=dt.datetime.now().strftime('%Y'), issue_date__month=dt.datetime.now().strftime('%m'), issue_date__day=dt.datetime.now().strftime('%d'))
            
            if 'token_type' in request.data:
                key = request.data['token_type'] + department.code
            else:
                key = 'N' + department.code 
                
            key = key + '{:>03}'.format(len(daily_tokens)) if len(department.code) == 2 else department.code + '{:>04}'.format(len(daily_tokens))
            token_serializer.save(key=key)
            token_serializer.save()
            
            return Response(token_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(token_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, pk=None):
        return Response({'token': 'This method is not allowed.', 'available methods': {'/start_attendence', '/end_attendence'}}, status=status.HTTP_400_BAD_REQUEST)


    def partial_update(self, request, pk=None):
        return Response({'token': 'This method is not allowed.', 'available methods': {'/start_attendence', '/end_attendence'}}, status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, pk=None):
        return Response({'token': 'This method is not allowed.', 'available methods': {'/end_attendence'}}, status=status.HTTP_400_BAD_REQUEST)
    
    
    @action(methods=['put'], detail=True,)
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


    @action(methods=['put'], detail=True,)
    def end_attendence(self, request, pk=None):
        token = self.get_object()
        
        if 'service' in request.data:
            service = Service.objects.filter(pk=request.data['service'])
            if service:
                token = self.get_object()
                if token.status == 'IAT':
                    token.status = 'TAR'
                    token.archived_date = dt.datetime.now(tz=timezone.utc) 
                    token.time_in_attendence = token.archived_date - token.attendence_date
                    token.service = service[0]
                    token.save()
                    response = TokenSerializer(token).data 
                elif token.status == 'TIS':
                    raise AttendenceNotStartedException()
                elif token.status == 'TAR':
                    raise TokenAlreadyArchivedException() 
                return Response(response) 
            else:
                return Response({'status': 'Service doesn\'t exist.'}, status=status.HTTP_400_BAD_REQUEST) 
        else:
            return Response({'status': 'This method requires \'service\' field.'}, status=status.HTTP_400_BAD_REQUEST) 


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
        
        if token.status != 'TIS':
            response = UserSerializer(token.clerk).data 
        else:
            raise AttendenceNotStartedException

        return Response(response) 

        