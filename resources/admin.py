from django.contrib import admin

from .models import Allocation, Resource

admin.site.register(Resource)
admin.site.register(Allocation)
