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
        shortage = max(demand - res.stock, 0)
        rows.append({"resource": res, "demand": demand, "shortage": shortage,
                     "spare": max(res.stock - demand, 0), "status": stock_status(res, shortage)})
    return rows


def stock_status(res, shortage):
    """'short' if open demand exceeds stock, 'low' if under half of capacity, else 'ok'."""
    if shortage:
        return "short"
    return "low" if res.capacity and res.stock * 2 < res.capacity else "ok"


def overview(rows):
    """Headline numbers for the Resources page hero: counts plus overall stock level."""
    stock = sum(r["resource"].stock for r in rows)
    cap = sum(r["resource"].capacity for r in rows)
    return {"total": len(rows),
            "covered": sum(1 for r in rows if r["status"] == "ok"),
            "restock": sum(1 for r in rows if r["status"] != "ok"),
            "stock": stock, "capacity": cap,
            "percent": min(100, round(100 * stock / cap)) if cap else 0}



def consume(relief_request):
    """Called on delivery: take the allocated units out of stock."""
    for a in relief_request.allocations.select_related("resource"):
        a.resource.stock = max(a.resource.stock - a.quantity, 0)
        a.resource.save(update_fields=["stock"])
