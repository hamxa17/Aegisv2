from django.db import models

from reliefrequests.models import ReliefRequest


class Resource(models.Model):
    name = models.CharField(max_length=60)
    need_type = models.CharField(max_length=10, choices=ReliefRequest.Need.choices, unique=True)
    stock = models.PositiveIntegerField(default=0)
    capacity = models.PositiveIntegerField(default=0, help_text="Stock level considered 'full'")

    def __str__(self):
        return self.name

    @property
    def percent(self):
        return min(100, round(100 * self.stock / self.capacity)) if self.capacity else 0


class Allocation(models.Model):
    request = models.ForeignKey(ReliefRequest, on_delete=models.CASCADE, related_name="allocations")
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name="allocations")
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
