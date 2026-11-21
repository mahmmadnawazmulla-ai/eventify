from django.urls import path
from . import views
urlpatterns = [
    path("register/<int:pk>/", views.register, name="register"), path("cancel/<int:pk>/", views.cancel, name="cancel"),
    path("mine/", views.my_registrations, name="my_registrations"), path("manage/", views.manage, name="manage_registrations"),
    path("manage/<int:pk>/<str:action>/", views.set_status, name="set_status")]
