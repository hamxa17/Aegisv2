from django.urls import path

from . import views

urlpatterns = [
    path("", views.resource_list, name="resources"),
    path("new/", views.create_resource, name="create_resource"),
    path("<int:pk>/edit/", views.edit_resource, name="edit_resource"),
    path("<int:pk>/delete/", views.delete_resource, name="delete_resource"),
    path("<int:pk>/stock/", views.update_stock, name="update_stock"),
    path("save-all/", views.update_all_stock, name="update_all_stock"),
    path("allocate/", views.run_allocation, name="run_allocation"),
]
