from django.db import models
from services.models import Service

class Department(models.Model):
    name = models.CharField(max_length=100)
    available_services = models.ManyToManyField(Service)

    def __str__(self):
        return self.name
