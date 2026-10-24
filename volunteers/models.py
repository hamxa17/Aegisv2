from django.conf import settings
from django.db import models

from reliefrequests.models import ReliefRequest


class Assignment(models.Model):
    request = models.OneToOneField(ReliefRequest, on_delete=models.CASCADE, related_name="assignment")
    volunteer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="assignments")
    assigned_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    note = models.CharField(max_length=200, blank=True)
