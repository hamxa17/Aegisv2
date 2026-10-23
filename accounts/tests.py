# Account tests. Owner: Amrin
from django.test import TestCase
from django.urls import reverse

from .models import User


class AccountTests(TestCase):
    def test_register_logs_in_and_routes_by_role(self):
        r = self.client.post(reverse("register"), {
            "full_name": "Rina", "email": "rina@x.com", "phone": "01700000000",
            "role": "volunteer", "password1": "StrongPass123", "password2": "StrongPass123"})
        self.assertRedirects(r, reverse("home_redirect"), fetch_redirect_response=False)
        self.assertEqual(User.objects.get().role, "volunteer")

    def test_cannot_self_register_as_coordinator(self):
        r = self.client.post(reverse("register"), {
            "full_name": "X", "email": "x@x.com", "phone": "1", "role": "coordinator",
            "password1": "StrongPass123", "password2": "StrongPass123"})
        self.assertEqual(r.status_code, 200)
        self.assertFalse(User.objects.exists())
