# Photos app (media CRUD). Owner: Amrin
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import role_required
from reliefrequests.models import ReliefRequest
from .forms import PhotoForm
from .models import RequestPhoto


def visible_request(user, pk):
    obj = get_object_or_404(ReliefRequest, pk=pk)
    if user.role == "affected" and obj.requester_id != user.id:
        raise PermissionDenied
    return obj


def changeable_photo(user, pk):
    photo = get_object_or_404(RequestPhoto.objects.select_related("request"), pk=pk)
    visible_request(user, photo.request_id)
    if not photo.can_change(user):
        raise PermissionDenied
    return photo


@role_required("affected", "coordinator")
def photo_list(request, pk):
    obj = visible_request(request.user, pk)
    form = PhotoForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        photo = form.save(commit=False)
        photo.request, photo.uploaded_by = obj, request.user
        photo.save()
        messages.success(request, "Photo uploaded.")
        return redirect("photo_list", pk=obj.pk)
    photos = obj.photos.select_related("uploaded_by")
    return render(request, "photos/photo_list.html", {"obj": obj, "photos": photos, "form": form})


@role_required("affected", "coordinator")
def photo_edit(request, pk):
    photo = changeable_photo(request.user, pk)
    old_file = photo.image.name
    form = PhotoForm(request.POST or None, request.FILES or None, instance=photo)
    if request.method == "POST" and form.is_valid():
        updated = form.save()
        if updated.image.name != old_file:
            updated.image.storage.delete(old_file)
        messages.success(request, "Photo updated.")
        return redirect("photo_list", pk=photo.request_id)
    return render(request, "photos/photo_form.html", {"photo": photo, "form": form})


@role_required("affected", "coordinator")
def photo_delete(request, pk):
    photo = changeable_photo(request.user, pk)
    if request.method == "POST":
        request_id = photo.request_id
        photo.image.delete(save=False)
        photo.delete()
        messages.success(request, "Photo deleted.")
        return redirect("photo_list", pk=request_id)
    return render(request, "photos/photo_confirm_delete.html", {"photo": photo})
