from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from accounts.models import User
from .models import ReliefRequest
from .scoring import calculate_priority


class ScoringTests(SimpleTestCase):
    def test_proposal_example_is_critical_9(self):
        self.assertEqual(calculate_priority(no_supplies=True, household_size=60, vulnerable=True), (9, "critical"))

    def test_normal_request_scores_one(self):
        self.assertEqual(calculate_priority(), (1, "low"))

    def test_band_edges(self):
        self.assertEqual(calculate_priority(medical=True)[1], "high")          # 5
        self.assertEqual(calculate_priority(household_size=51)[1], "medium")   # 3
        self.assertEqual(calculate_priority(medical=True, no_supplies=True)[1], "critical")  # 9

    def test_fifty_is_not_large(self):
        self.assertEqual(calculate_priority(household_size=50)[0], 1)


class ReliefRequestModelTests(TestCase):
    def setUp(self):
        self.family = User.objects.create_user("f@x.com", password="x")

    def test_priority_is_calculated_on_save(self):
        r = ReliefRequest.objects.create(requester=self.family, location="A", need_type="water",
                                         household_size=60, no_supplies=True, has_vulnerable=True)
        self.assertEqual((r.priority_score, r.priority_band), (9, "critical"))

    def test_default_ordering_is_highest_priority_first(self):
        ReliefRequest.objects.create(requester=self.family, location="A", need_type="food")
        urgent = ReliefRequest.objects.create(requester=self.family, location="B", need_type="medicine", medical_emergency=True)
        self.assertEqual(ReliefRequest.objects.first(), urgent)


class RequestViewTests(TestCase):
    DATA = {"location": "Bagerpara", "household_size": 4, "need_type": "water", "quantity": 10,
            "description": "", "medical_emergency": "on"}

    def setUp(self):
        self.family = User.objects.create_user("f@x.com", password="x")
        self.other = User.objects.create_user("o@x.com", password="x")
        self.coord = User.objects.create_user("c@x.com", password="x", role="coordinator")

    def test_family_can_submit_a_request(self):
        self.client.force_login(self.family)
        r = self.client.post(reverse("submit_request"), self.DATA)
        self.assertRedirects(r, reverse("my_requests"))
        req = ReliefRequest.objects.get()
        self.assertEqual((req.requester, req.priority_band), (self.family, "high"))

    def test_zero_people_is_rejected(self):
        self.client.force_login(self.family)
        self.client.post(reverse("submit_request"), {**self.DATA, "household_size": 0})
        self.assertFalse(ReliefRequest.objects.exists())

    def test_coordinator_cannot_submit(self):
        self.client.force_login(self.coord)
        self.assertEqual(self.client.get(reverse("submit_request")).status_code, 403)

    def test_my_requests_shows_only_own_requests(self):
        ReliefRequest.objects.create(requester=self.other, location="Secret", need_type="food")
        mine = ReliefRequest.objects.create(requester=self.family, location="Mine", need_type="food")
        self.client.force_login(self.family)
        page = self.client.get(reverse("my_requests"))
        self.assertEqual(list(page.context["reqs"]), [mine])
