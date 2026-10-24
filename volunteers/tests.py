from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from reliefrequests.models import ReliefRequest
from resources.models import Resource
from .models import Assignment


class DeliveryTests(TestCase):
    def test_volunteer_delivery_updates_status_and_stock(self):
        fam = User.objects.create_user("f@x.com", password="x")
        vol = User.objects.create_user("v@x.com", password="x", role="volunteer")
        Resource.objects.create(name="Water", need_type="water", stock=100, capacity=100)
        req = ReliefRequest.objects.create(requester=fam, location="A", need_type="water", quantity=40, status="assigned")
        from resources.allocation import run_allocation
        run_allocation()
        a = Assignment.objects.create(request=req, volunteer=vol)
        self.client.force_login(vol)
        self.client.post(reverse("mark_delivered", args=[a.pk]))
        req.refresh_from_db()
        self.assertEqual(req.status, "delivered")
        self.assertEqual(Resource.objects.get().stock, 60)

    def test_family_cannot_open_volunteer_page(self):
        self.client.force_login(User.objects.create_user("f@x.com", password="x"))
        self.assertEqual(self.client.get(reverse("tasks")).status_code, 403)
