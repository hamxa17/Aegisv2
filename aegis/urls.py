from django.conf import settings  # Added by Sunita: media settings
from django.conf.urls.static import static  # Added by Sunita: serves uploaded photos
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
    path("photos/", include("photos.urls")),  # Added by Sunita: photo pages
    path("", include("volunteers.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Added by Sunita: show uploaded photos
