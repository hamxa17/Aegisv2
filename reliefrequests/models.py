from django.conf import settings
from django.db import models

from .scoring import calculate_priority


class ReliefRequest(models.Model):
    class Need(models.TextChoices):
        FOOD = "food", "Food packets"
        WATER = "water", "Drinking water"
        MEDICINE = "medicine", "Medicine"
        SHELTER = "shelter", "Blankets / shelter"

    class Status(models.TextChoices):
        PENDING = "pending", "Awaiting verification"
        VERIFIED = "verified", "Verified"
        ASSIGNED = "assigned", "Assigned to volunteer"
        DELIVERED = "delivered", "Delivered"
        REJECTED = "rejected", "Rejected"

    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="relief_requests")
    location = models.CharField(max_length=200)
    household_size = models.PositiveIntegerField(default=1)
    need_type = models.CharField(max_length=10, choices=Need.choices)
    quantity = models.PositiveIntegerField(default=1, help_text="Units needed (packets, bottles, kits, blankets)")
    description = models.TextField(blank=True)
    medical_emergency = models.BooleanField(default=False)
    no_supplies = models.BooleanField("No food or water at hand", default=False)
    has_vulnerable = models.BooleanField("Children or elderly present", default=False)

    priority_score = models.PositiveSmallIntegerField(default=1, editable=False)
    priority_band = models.CharField(max_length=10, default="low", editable=False)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    verified_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="+")
    verified_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-priority_score", "created_at"]

    def save(self, *args, **kwargs):
        self.priority_score, self.priority_band = calculate_priority(
            medical=self.medical_emergency, no_supplies=self.no_supplies,
            household_size=self.household_size, vulnerable=self.has_vulnerable)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"#{self.pk} {self.get_need_type_display()} — {self.location}"
