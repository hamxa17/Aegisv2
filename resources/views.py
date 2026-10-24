from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from accounts.decorators import role_required
from . import allocation
from .models import Resource


@role_required("coordinator")
def resource_list(request):
    rows = allocation.summary()
    return render(request, "resources/resources.html", {"rows": rows, "stats": allocation.overview(rows)})


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
def run_allocation(request):
    allocation.run_allocation()
    messages.success(request, "Allocation recalculated by priority.")
    return redirect("resources")
