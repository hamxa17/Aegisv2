from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("requests/", include("reliefrequests.urls")),
    path("coordinator/", include("coordination.urls")),
    path("resources/", include("resources.urls")),
    path("", include("volunteers.urls")),
]
