# solicitud_adopcion/urls.py
from django.urls import path
from . import views

app_name = "solicitud_adopcion"

urlpatterns = [
    path("", views.lista_solicitudes, name="lista_solicitudes"),
    path("<int:solicitud_id>/", views.detalle_solicitud, name="detalle_solicitud"),
    path("<int:solicitud_id>/responder/", views.responder_solicitud, name="responder_solicitud"),
    # 👉 Nueva ruta para la solicitud directa desde la tarjeta de mascota
    path("rapida/<int:mascota_id>/", views.crear_solicitud_rapida, name="crear_rapida"),
]