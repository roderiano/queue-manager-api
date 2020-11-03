from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from .models import Service
from .serializers import ServiceSerializer


class GetAllServicesTest(TestCase):
    
    def setUp(self):
        self.client = APIClient()

        User.objects.create(username='admin', password='admin')
        token = Token.objects.get(user__username='admin')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        Service.objects.create(name='Service 1',)
        Service.objects.create(name='Service 2',)
        Service.objects.create(name='Service 3',)
        Service.objects.create(name='Service 4',)

    def test_all_services_get(self):
        serializer = ServiceSerializer(Service.objects.all(), many=True)
        response = self.client.get('/services/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


class GetSingleServiceTest(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.service = Service.objects.create(name='Service 1',)

        User.objects.create(username='admin', password='admin')
        token = Token.objects.get(user__username='admin')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)


    def test_single_service_get(self):
        serializer = ServiceSerializer(self.service, many=False)
        response = self.client.get('/services/' + str(self.service.pk) + '/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        
    
    def test_invalid_single_service_get(self):
        serializer = ServiceSerializer(self.service, many=False)
        response = self.client.get('/services/0/')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PostSingleServiceTest(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        User.objects.create(username='admin', password='admin', is_superuser=True,)
        token = Token.objects.get(user__username='admin')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    
    def test_single_service_post(self):
        response = self.client.post('/services/', {'name': 'Service 1'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_single_service_post(self):
        response = self.client.post('/services/', {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSingleServiceTest(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.service = Service.objects.create(name='Service 1',)

        User.objects.create(username='admin', password='admin', is_superuser=True,)
        token = Token.objects.get(user__username='admin')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    
    def test_single_service_delete(self):
        response = self.client.delete('/services/' + str(self.service.pk) + '/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_single_service_delete(self):
        response = self.client.post('/services/0/')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class PutSingleServiceTest(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.service = Service.objects.create(name='Service 1',)

        User.objects.create(username='admin', password='admin', is_superuser=True,)
        token = Token.objects.get(user__username='admin')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    
    def test_single_service_put(self):
        response = self.client.put('/services/' + str(self.service.pk) + '/', {'name': 'Service 2'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_single_service_put(self):
        response = self.client.put('/services/0/', {'name': 'Service 2'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
