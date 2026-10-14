# Demo data for presentations. Owner: Amrin
from django.core.management.base import BaseCommand

from accounts.models import User
from reliefrequests.models import ReliefRequest
from resources.models import Resource

PASSWORD = "aegis1234"


class Command(BaseCommand):
    help = "Create demo resources, users and requests for presentations."

    def handle(self, *args, **opts):
        for name, need, stock, cap in [("Food packets", "food", 350, 500), ("Water bottles", "water", 200, 500),
                                       ("Medicine kits", "medicine", 140, 200), ("Blankets", "shelter", 260, 300)]:
            Resource.objects.update_or_create(need_type=need, defaults={"name": name, "stock": stock, "capacity": cap})
        users = {}
        for email, name, role in [("coord@aegis.test", "Coordinator Demo", "coordinator"), ("volunteer@aegis.test", "Fahim R.", "volunteer"),
                                  ("family@aegis.test", "Amrin", "affected")]:
            u, made = User.objects.get_or_create(username=email, defaults={"email": email, "first_name": name, "role": role})
            if made:
                u.set_password(PASSWORD); u.save()
            users[role] = u
        if not ReliefRequest.objects.exists():
            fam = users["affected"]
            for loc, need, qty, size, kw in [
                ("Bagerpara", "medicine", 10, 4, {"medical_emergency": True}),
                ("Shibganj", "water", 200, 60, {"no_supplies": True, "has_vulnerable": True}),
                ("Char Rajibpur", "medicine", 5, 3, {"has_vulnerable": True, "no_supplies": True}),
                ("Bagerpara", "food", 30, 30, {}),
                ("Shibganj", "shelter", 6, 6, {})]:
                ReliefRequest.objects.create(requester=fam, location=loc, need_type=need, quantity=qty, household_size=size, **kw)
        self.stdout.write(self.style.SUCCESS(f"Demo data ready. Logins: coord@aegis.test / volunteer@aegis.test / family@aegis.test  password: {PASSWORD}"))
        