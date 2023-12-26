from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from etienda.api import api

urlpatterns = [
    path("etienda/", include("etienda.urls")),
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("api/", api.urls),
]

if settings.DEBUG: 
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)