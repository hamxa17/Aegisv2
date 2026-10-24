from django.contrib import admin

from .models import RequestPhoto


@admin.register(RequestPhoto)
class RequestPhotoAdmin(admin.ModelAdmin):
    list_display = ("id", "request", "caption", "uploaded_by", "uploaded_at")
    list_filter = ("uploaded_at",)
    search_fields = ("caption", "request__location")
