from django.contrib.auth import views as auth
from django.urls import path
from . import views
urlpatterns = [
    path("login/", auth.LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path("logout/", auth.LogoutView.as_view(), name="logout"),
    path("signup/", views.signup, name="signup"), path("profile/", views.profile, name="profile")]
