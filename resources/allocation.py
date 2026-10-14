"""Priority-based allocation: higher-priority requests are served first; ties go to the older request."""
from django.db import transaction
from django.db.models import Sum

from reliefrequests.models import ReliefRequest
from .models import Allocation, Resource

OPEN = (ReliefRequest.Status.VERIFIED, ReliefRequest.Status.ASSIGNED)


def plan_allocation(demands, stock):
    """demands: [(id, qty)] already in priority order -> [(id, given)]. Pure function, easy to test."""
    plan, left = [], stock
    for key, qty in demands:
        give = min(qty, left)
        plan.append((key, give))
        left -= give
    return plan


def run_allocation():
    """Recompute the allocation plan for all open (verified/assigned) requests."""
    with transaction.atomic():
        Allocation.objects.all().delete()
        for res in Resource.objects.all():
            reqs = ReliefRequest.objects.filter(status__in=OPEN, need_type=res.need_type)  # Meta ordering = priority
            plan = plan_allocation([(r.pk, r.quantity) for r in reqs], res.stock)
            Allocation.objects.bulk_create(
                Allocation(request_id=pk, resource=res, quantity=give) for pk, give in plan if give > 0)


def summary():
    rows = []
    for res in Resource.objects.all():
        demand = ReliefRequest.objects.filter(status__in=OPEN, need_type=res.need_type).aggregate(s=Sum("quantity"))["s"] or 0
        rows.append({"resource": res, "demand": demand, "shortage": max(demand - res.stock, 0)})
    return rows
