from django.db import models
from departments.models import Departament
import datetime

class Token(models.Model):

    STATUS_TYPES = [('TIS', 'TOKEN ISSUED'),
                    ('IAT', 'IN ATTENDENCE'),
                    ('TAR', 'TOKEN ARCHIVED')]

    actived = models.BooleanField(default=True)
    status = models.CharField(max_length=3, choices=STATUS_TYPES, default='TIS')
    departament = models.ForeignKey(Departament, on_delete=models.CASCADE)
    issue_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.status
