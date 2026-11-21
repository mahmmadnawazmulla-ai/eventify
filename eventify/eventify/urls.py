from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
urlpatterns = [path("django-admin/", admin.site.urls), path("accounts/", include("accounts.urls")),
    path("registrations/", include("registrations.urls")), path("dashboard/", include("dashboard.urls")),
    path("", include("events.urls"))] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
