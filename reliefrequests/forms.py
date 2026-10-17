from django import forms

from .models import ReliefRequest


class ReliefRequestForm(forms.ModelForm):
    class Meta:
        model = ReliefRequest
        fields = ["location", "household_size", "need_type", "quantity", "description",
                  "medical_emergency", "no_supplies", "has_vulnerable"]
        widgets = {"description": forms.Textarea(attrs={"rows": 3}), "location": forms.TextInput(attrs={"placeholder": "Village / ward / landmark"})}
        labels = {"household_size": "People affected", "need_type": "Primary need", "quantity": "Units needed",
                  "description": "What's the situation?"}

    def clean(self):
        data = super().clean()
        for f in ("household_size", "quantity"):
            if data.get(f) is not None and data[f] < 1:
                self.add_error(f, "Must be at least 1.")
        return data
