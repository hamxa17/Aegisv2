from django.contrib import messages
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from accounts.decorators import role_required
from reliefrequests.models import ReliefRequest
from resources.allocation import consume
from .forms import ProofForm
from .models import Assignment

S = ReliefRequest.Status


@role_required("volunteer")
def tasks(request):
    mine = request.user.assignments.select_related("request").order_by("delivered_at", "-request__priority_score")
    return render(request, "volunteers/tasks.html", {"todo": [a for a in mine if not a.delivered_at], "done": [a for a in mine if a.delivered_at]})


@role_required("volunteer")
@require_POST
def mark_delivered(request, pk):
    a = get_object_or_404(Assignment, pk=pk, volunteer=request.user, delivered_at__isnull=True)
    a.delivered_at = timezone.now()
    a.note = request.POST.get("note", "")[:200]
    proof = ProofForm(request.POST, request.FILES)
    if proof.is_valid() and proof.cleaned_data["proof"]:
        a.proof = proof.cleaned_data["proof"]
    elif proof.errors:
        messages.error(request, proof.errors["proof"][0])
        return redirect("tasks")
    a.save()
    a.request.status = S.DELIVERED
    a.request.save()
    consume(a.request)
    messages.success(request, "Marked as delivered. Thank you!")
    return redirect("tasks")


@role_required("volunteer")
@require_POST
def replace_proof(request, pk):
    a = get_object_or_404(Assignment, pk=pk, volunteer=request.user, delivered_at__isnull=False)
    form = ProofForm(request.POST, request.FILES)
    if form.is_valid() and form.cleaned_data["proof"]:
        if a.proof:
            a.proof.delete(save=False)
        a.proof = form.cleaned_data["proof"]
        a.save()
        messages.success(request, "Delivery photo updated.")
    else:
        messages.error(request, form.errors.get("proof", ["Choose a photo first."])[0])
    return redirect("tasks")


@role_required("volunteer")
@require_POST
def remove_proof(request, pk):
    a = get_object_or_404(Assignment, pk=pk, volunteer=request.user, delivered_at__isnull=False)
    if a.proof:
        a.proof.delete(save=False)
        a.proof = ""
        a.save()
        messages.success(request, "Delivery photo removed.")
    return redirect("tasks")


@role_required("coordinator")
def reports(request):
    total = ReliefRequest.objects.count()
    by_band = {b["priority_band"]: b["n"] for b in ReliefRequest.objects.values("priority_band").annotate(n=Count("id"))}
    by_status = {s["status"]: s["n"] for s in ReliefRequest.objects.values("status").annotate(n=Count("id"))}
    bands = [(b.title(), by_band.get(b, 0), b) for b in ("critical", "high", "medium", "low")]
    statuses = [(label, by_status.get(val, 0)) for val, label in S.choices]
    done = by_status.get(S.DELIVERED, 0)
    return render(request, "volunteers/reports.html", {
        "total": total, "bands": bands, "statuses": statuses,
        "rate": round(100 * done / total) if total else 0, "max_band": max([n for _, n, _ in bands] + [1])})
