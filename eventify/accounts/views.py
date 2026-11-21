from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import SignUpForm, ProfileForm

def signup(request):
    form = SignUpForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.save()); messages.success(request, "Welcome to Eventify!")
        return redirect("dashboard")
    return render(request, "accounts/signup.html", {"form": form})

@login_required
def profile(request):
    form = ProfileForm(request.POST or None, instance=request.user.profile)
    if request.method == "POST" and form.is_valid():
        form.save(); messages.success(request, "Profile updated."); return redirect("profile")
    return render(request, "accounts/profile.html", {"form": form})
