from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib import messages
from .forms import RegisterForm, ProfileForm
# from .forms import RegisterForm

HOME = {"affected": "my_requests", "volunteer": "tasks", "coordinator": "coord_dashboard"}


def register(request):
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.save())
        return redirect("home_redirect")
    return render(request, "accounts/register.html", {"form": form})


@login_required
def home_redirect(request):
    return redirect(HOME[request.user.role])

def profile(request):
    form = ProfileForm(request.POST or None, instance=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Profile updated.")
        return redirect("profile")
    return render(request, "accounts/profile.html", {"form": form})