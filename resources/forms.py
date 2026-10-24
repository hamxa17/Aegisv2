from django import forms

from .models import Resource


class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ["name", "need_type", "stock", "capacity"]

    def clean(self):
        data = super().clean()
        stock, cap = data.get("stock"), data.get("capacity")
        if stock is not None and cap is not None and stock > cap:
            raise forms.ValidationError("Stock cannot be more than capacity.")
        return data
