from django.urls import path
from django.views.generic import TemplateView
from . import views
urlpatterns = [
    path("", views.home, name="home"), path("about/", TemplateView.as_view(template_name="about.html"), name="about"),
    path("events/", views.event_list, name="events"), path("events/new/", views.event_create, name="event_create"),
    path("events/<int:pk>/", views.event_detail, name="event_detail"),
    path("events/<int:pk>/edit/", views.event_edit, name="event_edit"),
    path("events/<int:pk>/delete/", views.event_delete, name="event_delete")]
