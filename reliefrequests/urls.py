from django.urls import path

from . import views

urlpatterns = [
    path("new/", views.submit_request, name="submit_request"),
    path("mine/", views.my_requests, name="my_requests"),
]
