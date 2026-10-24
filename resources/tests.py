from django.test import SimpleTestCase, TestCase

from accounts.models import User
from reliefrequests.models import ReliefRequest
from .allocation import overview, plan_allocation, run_allocation, summary
from .models import Allocation, Resource


class PlanTests(SimpleTestCase):
    def test_proposal_water_example(self):
        # 500 bottles; Critical 200, High 150, Medium 300 -> 650 needed, 150 short
        self.assertEqual(plan_allocation([(1, 200), (2, 150), (3, 300)], 500), [(1, 200), (2, 150), (3, 150)])


class AllocationDbTests(TestCase):
    def test_priority_first_and_shortage(self):
        u = User.objects.create_user("f@x.com", password="x")
        Resource.objects.create(name="Water bottles", need_type="water", stock=500, capacity=500)
        mk = lambda qty, **kw: ReliefRequest.objects.create(requester=u, location="A", need_type="water", quantity=qty, status="verified", **kw)
        mk(300)                                                      # low priority, oldest
        mk(200, medical_emergency=True, no_supplies=True)            # critical
        run_allocation()
        self.assertEqual(Allocation.objects.get(request__priority_band="critical").quantity, 200)
        self.assertEqual(Allocation.objects.get(request__priority_band="low").quantity, 300)
        self.assertEqual(summary()[0]["shortage"], 0)


class StatusTests(TestCase):
    def test_status_and_overview(self):
        u = User.objects.create_user("g@x.com", password="x")
        Resource.objects.create(name="Water bottles", need_type="water", stock=120, capacity=500)
        Resource.objects.create(name="Food packets", need_type="food", stock=400, capacity=500)
        Resource.objects.create(name="Medicine kits", need_type="medicine", stock=60, capacity=200)
        ReliefRequest.objects.create(requester=u, location="A", need_type="water", quantity=200, status="verified")
        rows = {r["resource"].need_type: r for r in summary()}
        self.assertEqual(rows["water"]["status"], "short")
        self.assertEqual(rows["water"]["shortage"], 80)
        self.assertEqual(rows["food"]["status"], "ok")
        self.assertEqual(rows["food"]["spare"], 400)
        self.assertEqual(rows["medicine"]["status"], "low")
        self.assertEqual(overview(summary()), {"total": 3, "covered": 1, "restock": 2})


class ResourcePageTests(TestCase):
    def test_page_renders_chips_for_coordinator(self):
        coord = User.objects.create_user("c@x.com", password="x", role="coordinator")
        Resource.objects.create(name="Water bottles", need_type="water", stock=120, capacity=500)
        self.client.force_login(coord)
        page = self.client.get("/resources/")
        self.assertEqual(page.status_code, 200)
        self.assertContains(page, "resources tracked")
        self.assertContains(page, "Below half")


class ButtonTests(TestCase):
    def setUp(self):
        self.coord = User.objects.create_user("c2@x.com", password="x", role="coordinator")
        self.res = Resource.objects.create(name="Water", need_type="water", stock=100, capacity=500)

    def test_update_button(self):
        self.client.force_login(self.coord)
        r = self.client.post(f"/resources/{self.res.pk}/stock/", {"stock": "250"})
        self.assertEqual(r.status_code, 302)
        self.res.refresh_from_db(); self.assertEqual(self.res.stock, 250)

    def test_recalculate_button(self):
        self.client.force_login(self.coord)
        self.assertEqual(self.client.post("/resources/allocate/").status_code, 302)

    def test_non_coordinator_blocked(self):
        v = User.objects.create_user("v2@x.com", password="x", role="volunteer")
        self.client.force_login(v)
        self.client.post(f"/resources/{self.res.pk}/stock/", {"stock": "999"})
        self.res.refresh_from_db(); self.assertEqual(self.res.stock, 100)
