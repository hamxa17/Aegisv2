from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        AFFECTED = "affected", "Affected family"
        VOLUNTEER = "volunteer", "Volunteer"
        COORDINATOR = "coordinator", "Coordinator"

    role = models.CharField(max_length=12, choices=Role.choices, default=Role.AFFECTED)
    phone = models.CharField(max_length=20, blank=True)

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = self.Role.COORDINATOR
        super().save(*args, **kwargs)

    @property
    def display_name(self):
        return self.first_name or self.username
