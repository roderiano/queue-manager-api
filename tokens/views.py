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
import pytz
import datetime as dt
from rest_framework import status
from departments.models import Department
from profiles.models import Profile
from django.contrib.auth.models import User


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


    def get_queryset(self):
        if 'start_date' in self.request.query_params and 'end_date' in self.request.query_params:
            tokens = Token.objects.filter(issue_date__range=[self.request.query_params['start_date'], self.request.query_params['end_date']])
        else:
            tokens = Token.objects.all()

        return tokens


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
        user = request.user
        token = self.get_object()
        response = TokenSerializer(token).data

        tokens = Token.objects.filter(clerk=user, status='IAT')
        
        if len(tokens) > 0:
            token_data = TokenSerializer(tokens[0]).data
            return Response({'status': 'Clerk with another token in attendence.', 'token_in_attendence': token_data}, status=status.HTTP_303_SEE_OTHER)

        if token.status == 'TIS':
            token.status = 'IAT'
            token.attendence_date = dt.datetime.now(tz=pytz.utc) 
            token.time_waiting_attendence = token.attendence_date - token.issue_date
            token.clerk = user
            token.save()
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
                    token.archived_date = dt.datetime.now(tz=pytz.utc) 
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
                return Response({'service': 'Service doesn\'t exist.'}, status=status.HTTP_400_BAD_REQUEST) 
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

    @action(methods=['get'], detail=False,)
    def monitor(self, request):
        tokens = Token.objects.filter(attendence_date__year=dt.datetime.now().strftime('%Y'), 
                                      attendence_date__month=dt.datetime.now().strftime('%m'), 
                                      attendence_date__day=dt.datetime.now().strftime('%d'),
                                      status__in=['IAT', 'TAR']).order_by('-attendence_date')
        tokens = tokens[:5] if len(tokens) >= 5 else tokens[:len(tokens)]

        token_detail = []
        for token in tokens:
            place = Profile.objects.get(user=token.clerk).place
            token_detail.append({ 
                                    'key': token.key, 
                                    'place': place,
                                })
        
        serializer = TokenSerializer(tokens, many=True)

        return Response(token_detail)

    @action(methods=['get'], detail=False,)
    def dashboard_data(self, request):
        if 'start_date' in self.request.query_params and 'end_date' in self.request.query_params:
            tokens = Token.objects.filter(issue_date__range=[self.request.query_params['start_date'], self.request.query_params['end_date']])
            departments = Department.objects.all()
            services = Service.objects.all()
            clerks = User.objects.all()
        else:
            return Response({'start_date': 'Missing field start_date.'}, status=status.HTTP_400_BAD_REQUEST) if 'start_date' not in self.request.query_params else Response({'end_date': 'Missing field end_date.'}, status=status.HTTP_400_BAD_REQUEST) 

        # Get tokens amount per department
        departments_name = []
        for department in departments:
            if department.name not in departments_name:
                departments_name.append(department.name)

        total_tokens_per_department = [0] * len(departments_name)
        for token in tokens:
            total_tokens_per_department[departments_name.index(token.department.name)] += 1
        

        # Get service amount
        services_name = []
        for service in services:
            if service.name not in services_name:
                services_name.append(service.name)
        services_name.append('Unfinished Attendance')

        total_services = [0] * len(services_name)
        for token in tokens:
            if token.status == 'TAR':
                total_services[services_name.index(token.service.name)] += 1
            else:
                total_services[services_name.index('Unfinished Attendance')] += 1    


        # Get tokens amount per clerk
        clerks_name = []
        for clerk in clerks:
                clerks_name.append(clerk.username)

        total_tokens_per_clerk = [0] * len(clerks_name)
        for token in tokens:
            if token.status != 'TIS':
                total_tokens_per_clerk[clerks_name.index(token.clerk.username)] += 1

        
        # Total time per clerk
        total_time_per_clerk = [0] * len(clerks_name)
        for token in tokens:
            if token.status == 'TAR':
                total_time_per_clerk[clerks_name.index(token.clerk.username)] += token.time_in_attendence.seconds

        
        # General info
        total_tokens = len(tokens)
        average_in_attendance = dt.timedelta()
        average_waiting = dt.timedelta()

        for token in tokens:
            if token.status == 'TAR':
                average_in_attendance += token.time_in_attendence
        average_in_attendance = str(average_in_attendance / len(tokens)) if len(tokens) > 0 else "0:00:0.000000"

        for token in tokens:
            if token.status == 'TAR':
                average_waiting += token.time_waiting_attendence
        average_waiting = str(average_waiting / len(tokens)) if len(tokens) > 0 else "0:00:0.000000"


        return Response({'tokens_amount_per_department': {'labels': departments_name, 'data': total_tokens_per_department},
                         'services_amount': {'labels': services_name, 'data': total_services},
                         'tokens_amount_per_clerk': {'labels': clerks_name, 'data': total_tokens_per_clerk},
                         'total_time_per_clerk': {'labels': clerks_name, 'data': total_time_per_clerk},
                         'general_info': {'total_tokens': total_tokens, 'average_in_attendace': average_in_attendance, 'average_waiting': average_waiting},
                        })


        