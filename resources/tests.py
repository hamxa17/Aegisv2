from django.test import SimpleTestCase, TestCase

from accounts.models import User
from reliefrequests.models import ReliefRequest
from .allocation import plan_allocation, run_allocation, summary
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
