from django.test import SimpleTestCase

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
