from django.urls import path
from . import views

app_name = 'solicitud_adopcion'

urlpatterns = [
    path('', views.lista_solicitudes, name='lista_solicitudes'),
    path('nueva/', views.crear_solicitud, name='crear_solicitud'),
    path('<int:solicitud_id>/', views.detalle_solicitud, name='detalle_solicitud'),
    path('<int:solicitud_id>/responder/', views.responder_solicitud, name='responder_solicitud'),
]
