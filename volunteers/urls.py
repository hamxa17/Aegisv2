from django.urls import path

from . import views

urlpatterns = [
    path("volunteer/tasks/", views.tasks, name="tasks"),
    path("volunteer/tasks/<int:pk>/delivered/", views.mark_delivered, name="mark_delivered"),
    path("volunteer/tasks/<int:pk>/proof/", views.replace_proof, name="replace_proof"),
    path("volunteer/tasks/<int:pk>/proof/remove/", views.remove_proof, name="remove_proof"),
    path("reports/", views.reports, name="reports"),
]
