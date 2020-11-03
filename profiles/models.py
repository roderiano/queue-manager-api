from django.db import models
from django.contrib.auth.models import User
from departments.models import Department
from services.models import Service

class Profile(models.Model):
    place = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.place
        
