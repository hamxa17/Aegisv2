from django.urls import path

from . import views

urlpatterns = [
    path("volunteer/tasks/", views.tasks, name="tasks"),
    path("volunteer/tasks/<int:pk>/delivered/", views.mark_delivered, name="mark_delivered"),
    path("reports/", views.reports, name="reports"),
]
