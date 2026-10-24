from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from reliefrequests.models import ReliefRequest


class CoordinatorTests(TestCase):
    def setUp(self):
        self.fam = User.objects.create_user("f@x.com", password="x")
        self.coord = User.objects.create_user("c@x.com", password="x", role="coordinator")
        self.vol = User.objects.create_user("v@x.com", password="x", role="volunteer")
        self.req = ReliefRequest.objects.create(requester=self.fam, location="A", need_type="food")

    def test_verify_then_assign_flow(self):
        self.client.force_login(self.coord)
        self.client.post(reverse("coord_review", args=[self.req.pk]), {"action": "verify"})
        self.req.refresh_from_db(); self.assertEqual(self.req.status, "verified")
        self.client.post(reverse("coord_assign", args=[self.req.pk]), {"volunteer": self.vol.pk})
        self.req.refresh_from_db(); self.assertEqual(self.req.status, "assigned")
        self.assertEqual(self.req.assignment.volunteer, self.vol)

    def test_family_is_blocked(self):
        self.client.force_login(self.fam)
        self.assertEqual(self.client.get(reverse("coord_dashboard")).status_code, 403)
