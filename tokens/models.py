from django.db import models
from django.contrib.auth.models import User
from departments.models import Departament
from services.models import Service

class Token(models.Model):

    STATUS_TYPES = [('TIS', 'TOKEN ISSUED'),
                    ('IAT', 'IN ATTENDENCE'),
                    ('TAR', 'TOKEN ARCHIVED')]

    status = models.CharField(max_length=3, choices=STATUS_TYPES, default='TIS')
    departament = models.ForeignKey(Departament, on_delete=models.CASCADE)
    issue_date = models.DateTimeField(auto_now_add=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, blank=True, null=True)
    clerk = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.status
