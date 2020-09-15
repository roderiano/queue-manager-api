from django.db import models
from django.contrib.auth.models import User
from departments.models import Department
from services.models import Service

class Token(models.Model):

    STATUS_TYPES = [('TIS', 'TOKEN ISSUED'),
                    ('IAT', 'IN ATTENDENCE'),
                    ('TAR', 'TOKEN ARCHIVED')]

    status = models.CharField(max_length=3, choices=STATUS_TYPES, default='TIS')
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    issue_date = models.DateTimeField(auto_now_add=True, editable=False)
    attendence_date = models.DateTimeField(blank=True, null=True, editable=False)
    archived_date = models.DateTimeField(blank=True, null=True, editable=False)
    time_waiting_attendence = models.DurationField(blank=True, null=True, editable=False)
    time_in_attendence = models.DurationField(blank=True, null=True, editable=False)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, blank=True, null=True, editable=False)
    clerk = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, editable=False)

    def __str__(self):
        return self.status
