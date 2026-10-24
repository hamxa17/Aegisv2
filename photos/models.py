from django.conf import settings
from django.db import models

from reliefrequests.models import ReliefRequest


class RequestPhoto(models.Model):
    request = models.ForeignKey(ReliefRequest, on_delete=models.CASCADE, related_name="photos")
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name="photos")
    image = models.ImageField(upload_to="request_photos/%Y/%m/")
    caption = models.CharField(max_length=120, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_at"]

    def __str__(self):
        return f"Photo for request #{self.request_id}"

    def can_change(self, user):
        return user.role == "coordinator" or self.uploaded_by_id == user.id
