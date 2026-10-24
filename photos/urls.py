# Photos app (media CRUD). Owner: Amrin
from django.urls import path

from . import views

urlpatterns = [
    path("request/<int:pk>/", views.photo_list, name="photo_list"),
    path("<int:pk>/edit/", views.photo_edit, name="photo_edit"),
    path("<int:pk>/delete/", views.photo_delete, name="photo_delete"),
]
