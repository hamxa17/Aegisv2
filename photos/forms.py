# Photos app (media CRUD). Owner: Amrin
from django import forms

from .models import RequestPhoto

MAX_MB = 5


class PhotoForm(forms.ModelForm):
    class Meta:
        model = RequestPhoto
        fields = ["image", "caption"]
        labels = {"image": "Photo", "caption": "Caption (optional)"}
        widgets = {
            "image": forms.ClearableFileInput(attrs={"accept": "image/*", "data-preview": "photo-preview"}),
            "caption": forms.TextInput(attrs={"placeholder": "e.g. Water up to the doorstep"}),
        }

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if image and image.size > MAX_MB * 1024 * 1024:
            raise forms.ValidationError(f"Photo must be smaller than {MAX_MB} MB.")
        return image
