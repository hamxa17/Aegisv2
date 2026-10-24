from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name="coord_dashboard"),
    path("<int:pk>/review/", views.review, name="coord_review"),
    path("<int:pk>/assign/", views.assign, name="coord_assign"),
]
