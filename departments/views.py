from rest_framework.authentication import TokenAuthentication
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from services.serializers import ServiceSerializer
from api.permissions import IsAdminOrReadOnly
from .serializers import DepartmentSerializer
from .models import Department
from rest_framework import status


class DepartmentViewSet(ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAdminOrReadOnly,]

    # Method to list all availabe services at departmet
    @action(methods=['get'], detail=True,)
    def available_services(self, request, pk=None):
        department = self.get_object()
        serializer = ServiceSerializer(department.available_services.all(), many=True)

        return Response(serializer.data) 

    def create(self, request):
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            code = request.data['code'].upper()
            print(code)
            if len(Department.objects.filter(code=code)) == 0:
                serializer.save(code=code)
                return Response(serializer.data)
            else:
                return Response({'code': 'Code must be unique.',})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, pk=None):
        department = self.get_object()
        serializer = self.serializer_class(department, data=request.data,)

        if serializer.is_valid():
            code = str(request.data['code']).upper()
            department_temp = Department.objects.filter(code=code)
            if len(department_temp) == 1:
                if department_temp[0].id == department.id:
                    serializer.save(code=code)
                    return Response(serializer.data)
                    
            return Response({'code': 'Code must be unique.',})    
        else:
            return Response(serializer.errors)


    def partial_update(self, request, pk=None):
        return Response({ "detail":  "This action is not authorized." }, status=status.HTTP_400_BAD_REQUEST)