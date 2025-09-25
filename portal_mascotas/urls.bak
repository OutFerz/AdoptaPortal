# portal_mascotas/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('login.urls')),
    path('blog/', include('blog.urls')),
    path(
        "solicitudes/",
        include(("solicitud_adopcion.urls", "solicitud_adopcion"), namespace="solicitud_adopcion"),
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)