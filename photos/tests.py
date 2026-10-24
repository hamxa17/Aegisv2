# Photos app (media CRUD). Owner: Amrin
import shutil
import tempfile
from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from PIL import Image

from accounts.models import User
from reliefrequests.models import ReliefRequest
from .models import RequestPhoto

MEDIA = tempfile.mkdtemp()


def fake_image(name="flood.png", color="blue"):
    buf = BytesIO()
    Image.new("RGB", (20, 20), color).save(buf, "PNG")
    return SimpleUploadedFile(name, buf.getvalue(), content_type="image/png")


@override_settings(MEDIA_ROOT=MEDIA)
class PhotoCrudTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(MEDIA, ignore_errors=True)

    def setUp(self):
        self.fam = User.objects.create_user("f@x.com", password="x")
        self.req = ReliefRequest.objects.create(requester=self.fam, location="A", need_type="water", quantity=5)
        self.client.force_login(self.fam)

    def upload(self, caption="Doorstep"):
        return self.client.post(reverse("photo_list", args=[self.req.pk]), {"image": fake_image(), "caption": caption})

    def test_create_and_read(self):
        self.upload()
        self.assertEqual(self.req.photos.count(), 1)
        page = self.client.get(reverse("photo_list", args=[self.req.pk]))
        self.assertContains(page, "Doorstep")

    def test_update_caption_and_image(self):
        self.upload()
        photo = RequestPhoto.objects.get()
        old = photo.image.name
        self.client.post(reverse("photo_edit", args=[photo.pk]), {"image": fake_image("new.png", "red"), "caption": "Roof"})
        photo.refresh_from_db()
        self.assertEqual(photo.caption, "Roof")
        self.assertNotEqual(photo.image.name, old)

    def test_delete(self):
        self.upload()
        photo = RequestPhoto.objects.get()
        self.client.post(reverse("photo_delete", args=[photo.pk]))
        self.assertFalse(RequestPhoto.objects.exists())

    def test_photo_with_new_request(self):
        self.client.post(reverse("submit_request"), {"location": "B", "household_size": 3, "need_type": "food",
                                                     "quantity": 2, "image": fake_image(), "caption": "Kitchen"})
        self.assertEqual(RequestPhoto.objects.get().caption, "Kitchen")

    def test_other_family_is_blocked(self):
        other = User.objects.create_user("o@x.com", password="x")
        self.client.force_login(other)
        self.assertEqual(self.client.get(reverse("photo_list", args=[self.req.pk])).status_code, 403)

    def test_rejects_non_image(self):
        bad = SimpleUploadedFile("notes.txt", b"hello", content_type="text/plain")
        self.client.post(reverse("photo_list", args=[self.req.pk]), {"image": bad})
        self.assertFalse(RequestPhoto.objects.exists())
