from django.db import models
from profiles.models import Profile
from departments.models import Department
from services.models import Service

class Token(models.Model):

    STATUS_TYPES = [('TIS', 'TOKEN ISSUED'),
                    ('IAT', 'IN ATTENDENCE'),
                    ('TAR', 'TOKEN ARCHIVED')]

    status = models.CharField(max_length=3, choices=STATUS_TYPES, default='TIS')
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    issue_date = models.DateTimeField(auto_now_add=True)
    attendence_date = models.DateTimeField(blank=True, null=True)
    archived_date = models.DateTimeField(blank=True, null=True)
    time_waiting_attendence = models.DurationField(blank=True, null=True)
    time_in_attendence = models.DurationField(blank=True, null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, blank=True, null=True)
    clerk = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.status
