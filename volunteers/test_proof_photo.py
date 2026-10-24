# Delivery proof photo tests (media create / read / update / delete).
import io
import shutil
import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from PIL import Image

from accounts.models import User
from reliefrequests.models import ReliefRequest
from .models import Assignment

TEMP_MEDIA = tempfile.mkdtemp()


def fake_image(name="p.png"):
    buf = io.BytesIO()
    Image.new("RGB", (20, 20), "green").save(buf, "PNG")
    return SimpleUploadedFile(name, buf.getvalue(), content_type="image/png")


@override_settings(MEDIA_ROOT=TEMP_MEDIA)
class ProofPhotoTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(TEMP_MEDIA, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        self.vol = User.objects.create_user("v@x.com", "v@x.com", "pass12345", role="volunteer")
        fam = User.objects.create_user("f@x.com", "f@x.com", "pass12345")
        req = ReliefRequest.objects.create(
            requester=fam, need_type="water", quantity=2, household_size=3,
            location="Sylhet", status=ReliefRequest.Status.ASSIGNED)
        self.a = Assignment.objects.create(request=req, volunteer=self.vol)
        self.client.login(username="v@x.com", password="pass12345")

    def deliver(self, **extra):
        return self.client.post(reverse("mark_delivered", args=[self.a.pk]), {"note": "ok", **extra})

    def test_deliver_with_photo(self):
        self.deliver(proof=fake_image())
        self.a.refresh_from_db()
        self.assertTrue(self.a.delivered_at)
        self.assertTrue(self.a.proof.name.startswith("delivery_proofs/"))
        self.assertContains(self.client.get(reverse("tasks")), self.a.proof.url)

    def test_deliver_without_photo_still_works(self):
        self.deliver()
        self.a.refresh_from_db()
        self.assertTrue(self.a.delivered_at)
        self.assertFalse(self.a.proof)

    def test_bad_file_blocks_delivery(self):
        self.deliver(proof=SimpleUploadedFile("x.png", b"nope", content_type="image/png"))
        self.a.refresh_from_db()
        self.assertIsNone(self.a.delivered_at)

    def test_replace_and_remove(self):
        self.deliver(proof=fake_image("a.png"))
        self.a.refresh_from_db()
        old = self.a.proof.name
        self.client.post(reverse("replace_proof", args=[self.a.pk]), {"proof": fake_image("b.png")})
        self.a.refresh_from_db()
        self.assertNotEqual(old, self.a.proof.name)
        self.client.post(reverse("remove_proof", args=[self.a.pk]))
        self.a.refresh_from_db()
        self.assertFalse(self.a.proof)

    def test_other_volunteer_cannot_touch_photo(self):
        self.deliver(proof=fake_image())
        User.objects.create_user("w@x.com", "w@x.com", "pass12345", role="volunteer")
        self.client.login(username="w@x.com", password="pass12345")
        r = self.client.post(reverse("remove_proof", args=[self.a.pk]))
        self.assertEqual(r.status_code, 404)
