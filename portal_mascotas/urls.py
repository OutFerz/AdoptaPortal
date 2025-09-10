from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views  # home()

urlpatterns = [
    # Home pública con tarjetas de mascotas
    path("", views.home, name="home"),

    path("admin/", admin.site.urls),
    path("accounts/", include("login.urls")),
    path("blog/", include("blog.urls")),
    path("solicitudes/", include("solicitud_adopcion.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)