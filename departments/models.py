from django.db import models
from services.models import Service

class Departament(models.Model):
    name = models.CharField(max_length=100)
    services = models.ManyToManyField(Service)

    def __str__(self):
        return self.name
