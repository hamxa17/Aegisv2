from django.urls import path

from . import views

urlpatterns = [
    path("", views.resource_list, name="resources"),
    path("<int:pk>/stock/", views.update_stock, name="update_stock"),
    path("save-all/", views.update_all_stock, name="update_all_stock"),
    path("allocate/", views.run_allocation, name="run_allocation"),
]
