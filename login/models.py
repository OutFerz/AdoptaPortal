from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    """
    Modelo personalizado de usuario con campos básicos:
    - Nombre de usuario
    - Correo electrónico
    - Contraseña
    - Fecha de creación
    - Fecha de actualización
    """
    
    # Hacer el email obligatorio y único
    email = models.EmailField(
        unique=True,
        verbose_name='Correo electrónico'
    )
    
    # Fechas de seguimiento
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación'
    )
    
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name='Fecha de actualización'
    )
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return self.username
