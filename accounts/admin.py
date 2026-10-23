from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class AegisUserAdmin(UserAdmin):
    list_display = ("username", "first_name", "role", "phone")
    list_filter = ("role",)
    fieldsets = UserAdmin.fieldsets + (("Aegis", {"fields": ("role", "phone")}),)
