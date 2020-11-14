from django.db import models
from django.contrib.auth.models import User
from departments.models import Department
from services.models import Service

class Token(models.Model):

    STATUS_TYPES = [('TIS', 'TOKEN ISSUED'),
                    ('IAT', 'IN ATTENDENCE'),
                    ('TAR', 'TOKEN ARCHIVED')]
    
    TOKEN_TYPES = [('N', 'NORMAL'),
                    ('P', 'PREFERENTIAL')]

    key = models.CharField(max_length=6, blank=True, null=True,)
    status = models.CharField(max_length=3, choices=STATUS_TYPES, default='TIS',)
    department = models.ForeignKey(Department, on_delete=models.CASCADE,)
    issue_date = models.DateTimeField(auto_now_add=True,)
    attendence_date = models.DateTimeField(blank=True, null=True,)
    archived_date = models.DateTimeField(blank=True, null=True,)
    time_waiting_attendence = models.DurationField(blank=True, null=True,)
    time_in_attendence = models.DurationField(blank=True, null=True,)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, blank=True, null=True,)
    clerk = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,)
    token_type = models.CharField(max_length=1, choices=TOKEN_TYPES, default='N',)

    def __str__(self):
        return self.status
