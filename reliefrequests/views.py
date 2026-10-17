from django.contrib import messages
from django.shortcuts import redirect, render

from accounts.decorators import role_required
from .forms import ReliefRequestForm
from .models import ReliefRequest

S = ReliefRequest.Status
STEPS = [("Submitted", 0), ("Verified by coordinator", 1), ("Assigned to volunteer", 2), ("Delivered", 3)]
RANK = {S.PENDING: 0, S.VERIFIED: 1, S.ASSIGNED: 2, S.DELIVERED: 3}


@role_required("affected")
def submit_request(request):
    form = ReliefRequestForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        obj = form.save(commit=False)
        obj.requester = request.user
        obj.save()
        messages.success(request, f"Request submitted — priority {obj.priority_score} ({obj.priority_band.title()}).")
        return redirect("my_requests")
    return render(request, "relief/request_form.html", {"form": form})


@role_required("affected")
def my_requests(request):
    reqs = request.user.relief_requests.order_by("-created_at")
    latest = reqs.first()
    steps = []
    if latest and latest.status != S.REJECTED:
        steps = [{"title": t, "done": i <= RANK[latest.status]} for t, i in STEPS]
    stats = {
        "active": reqs.filter(status__in=[S.PENDING, S.VERIFIED, S.ASSIGNED]).count(),
        "waiting": reqs.filter(status=S.PENDING).count(),
        "delivered": reqs.filter(status=S.DELIVERED).count(),
    }
    return render(request, "relief/my_requests.html", {"reqs": reqs, "latest": latest, "steps": steps, "stats": stats})
