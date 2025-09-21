# registro_mascotas/urls.py
from django.urls import path
from . import views

app_name = 'registro_mascotas'

urlpatterns = [
    path('publicar/', views.publicar_mascota, name='publicar_mascota'),
]
