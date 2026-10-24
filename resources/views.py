from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from accounts.decorators import role_required
from . import allocation
from .forms import ResourceForm
from .models import Resource


@role_required("coordinator")
def resource_list(request):
    rows = allocation.summary()
    return render(request, "resources/resources.html", {"rows": rows, "stats": allocation.overview(rows)})


@role_required("coordinator")
def create_resource(request):
    form = ResourceForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        res = form.save()
        messages.success(request, f"{res.name} added.")
        return redirect("resources")
    return render(request, "resources/resource_form.html", {"form": form, "heading": "Add a resource"})


@role_required("coordinator")
def edit_resource(request, pk):
    res = get_object_or_404(Resource, pk=pk)
    form = ResourceForm(request.POST or None, instance=res)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, f"{res.name} updated.")
        return redirect("resources")
    return render(request, "resources/resource_form.html", {"form": form, "heading": f"Edit {res.name}"})


@role_required("coordinator")
def delete_resource(request, pk):
    res = get_object_or_404(Resource, pk=pk)
    if request.method == "POST":
        name = res.name
        res.delete()
        messages.success(request, f"{name} deleted.")
        return redirect("resources")
    return render(request, "resources/resource_confirm_delete.html", {"res": res})


@role_required("coordinator")
@require_POST
def update_stock(request, pk):
    res = get_object_or_404(Resource, pk=pk)
    try:
        res.stock = max(int(request.POST["stock"]), 0)
    except (KeyError, ValueError):
        messages.error(request, "Enter a whole number for stock.")
    else:
        res.save(update_fields=["stock"])
        messages.success(request, f"{res.name} stock updated to {res.stock}.")
    return redirect("resources")


@role_required("coordinator")
@require_POST
def update_all_stock(request):
    """Save every stock box on the page in one go (fields are named stock_<id>)."""
    changes = []
    for res in Resource.objects.all():
        raw = request.POST.get(f"stock_{res.pk}")
        if raw is None:
            continue
        try:
            value = max(int(raw), 0)
        except ValueError:
            messages.error(request, f"{res.name}: enter a whole number. Nothing was saved.")
            return redirect("resources")
        if value != res.stock:
            res.stock = value
            changes.append(res)
    with transaction.atomic():
        for res in changes:
            res.save(update_fields=["stock"])
    if changes:
        names = ", ".join(r.name for r in changes)
        messages.success(request, f"Saved {len(changes)} change{'s' if len(changes) != 1 else ''}: {names}.")
    else:
        messages.info(request, "No changes to save.")
    return redirect("resources")


@role_required("coordinator")
@require_POST
def run_allocation(request):
    allocation.run_allocation()
    messages.success(request, "Allocation recalculated by priority.")
    return redirect("resources")
