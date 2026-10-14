from django.contrib import admin

from .models import ReliefRequest


@admin.register(ReliefRequest)
class ReliefRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "need_type", "location", "priority_score", "priority_band", "status")
    list_filter = ("status", "priority_band", "need_type")
