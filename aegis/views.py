# Landing page statistics. Owner: Sunita
from django.shortcuts import render

from accounts.models import User
from reliefrequests.models import ReliefRequest


def index(request):
    total = ReliefRequest.objects.count()
    delivered = ReliefRequest.objects.filter(status=ReliefRequest.Status.DELIVERED).count()
    return render(request, "index.html", {
        "total": total,
        "delivered": delivered,
        "volunteers": User.objects.filter(role=User.Role.VOLUNTEER).count(),
    })
