from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from accounts.decorators import role_required
from accounts.models import User
from reliefrequests.models import ReliefRequest
from resources.allocation import run_allocation, summary
from volunteers.models import Assignment

S = ReliefRequest.Status
OPEN = [S.PENDING, S.VERIFIED, S.ASSIGNED]


@role_required("coordinator")
def dashboard(request):
    queue = ReliefRequest.objects.filter(status__in=OPEN).select_related("requester", "assignment__volunteer")
    return render(request, "coordination/dashboard.html", {
        "queue": queue,
        "volunteers": User.objects.filter(role=User.Role.VOLUNTEER),
        "stats": {
            "open": queue.count(),
            "critical": queue.filter(priority_band="critical", status__in=[S.PENDING, S.VERIFIED]).count(),
            "volunteers": User.objects.filter(role=User.Role.VOLUNTEER).count(),
        },
        "resource_rows": summary(),
        "shortage": sum(r["shortage"] for r in summary()),
    })


@role_required("coordinator")
@require_POST
def review(request, pk):
    obj = get_object_or_404(ReliefRequest, pk=pk, status=S.PENDING)
    obj.status = S.VERIFIED if request.POST.get("action") == "verify" else S.REJECTED
    obj.verified_by, obj.verified_at = request.user, timezone.now()
    obj.save()
    run_allocation()
    messages.success(request, f"Request #{obj.pk} {obj.get_status_display().lower()}.")
    return redirect("coord_dashboard")


@role_required("coordinator")
@require_POST
def assign(request, pk):
    obj = get_object_or_404(ReliefRequest, pk=pk, status=S.VERIFIED)
    volunteer = get_object_or_404(User, pk=request.POST.get("volunteer"), role=User.Role.VOLUNTEER)
    Assignment.objects.update_or_create(request=obj, defaults={"volunteer": volunteer})
    obj.status = S.ASSIGNED
    obj.save()
    messages.success(request, f"Request #{obj.pk} assigned to {volunteer.display_name}.")
    return redirect("coord_dashboard")
