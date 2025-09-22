# portal_mascotas/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from portal_mascotas import views as core_views

urlpatterns = [
    path("admin/", admin.site.urls),

    # Home
    path("", core_views.home, name="home"),

    # Publicar mascotas (selector + formulario + "mis publicaciones")
    path(
        "publicar/",
        include(("registro_mascotas.urls", "registro_mascotas"), namespace="registro_mascotas"),
    ),

    # Solicitudes de adopción (listado/creación, etc.)
    path(
        "solicitudes/",
        include(("solicitud_adopcion.urls", "solicitud_adopcion")),
    ),

    # Auth (login/logout/registro)
    path(
        "accounts/",
        include(("login.urls", "login"), namespace="login"),
    ),

    # Blog
    path(
        "blog/",
        include(("blog.urls", "blog")),
    ),
]

# Servir archivos de MEDIA en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
