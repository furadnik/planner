"""Main urls config."""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from events.views import EventsIndexView

urlpatterns = [
    path('admin/', admin.site.urls, name="admin"),
    path('', EventsIndexView.as_view(), name="index"),
    path('events/', include("events.urls")),
    path('accounts/', include("accounts.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
