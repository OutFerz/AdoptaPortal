# registro_mascotas/urls.py
from django.urls import path
from . import views

app_name = "registro_mascotas"

urlpatterns = [
    # /publicar/  → selector o formulario si ?modo=form
    path("", views.publicar_mascota, name="publicar_mascota"),

    # /publicar/mis-publicaciones/
    path("mis-publicaciones/", views.mis_solicitudes, name="mis_solicitudes"),
]