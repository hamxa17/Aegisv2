from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import User


class RegisterForm(UserCreationForm):
    full_name = forms.CharField(max_length=150)
    # Coordinators are created by an admin, never through public sign-up.
    role = forms.ChoiceField(
        choices=[(User.Role.AFFECTED, "Affected family"), (User.Role.VOLUNTEER, "Volunteer")],
        initial=User.Role.AFFECTED, widget=forms.RadioSelect,
    )

    class Meta:
        model = User
        fields = ("email", "phone", "role")

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(username__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email
        user.first_name = self.cleaned_data["full_name"]
        if commit:
            user.save()
        return user


class EmailLoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email")

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "phone")
        labels = {"first_name": "Full name"}