# registro_mascotas/models.py
from django.db import models
from django.conf import settings
from portal_mascotas.constantes import TIPOS_MASCOTA, SEXOS, ESTADOS_MASCOTA

class Mascota(models.Model):
    """
    Registro de mascotas disponibles para adopción.

    Campos alineados con la migración inicial del proyecto:
    - nombre, tipo (choices TIPOS_MASCOTA), raza, edad (en meses),
      sexo (choices SEXOS), descripcion, ubicacion, foto,
      estado (choices ESTADOS_MASCOTA, default 'disponible'),
      fecha_registro (auto), responsable (FK usuario).
    """
    nombre = models.CharField(max_length=100, help_text="Nombre de la mascota")
    tipo = models.CharField(max_length=10, choices=TIPOS_MASCOTA)
    raza = models.CharField(max_length=100)
    # En la migración aparece como entero en meses. Mantener consistencia:
    edad = models.PositiveIntegerField(help_text="Edad en meses")
    sexo = models.CharField(max_length=10, choices=SEXOS)
    descripcion = models.TextField(help_text="Descripción de la mascota")
    ubicacion = models.CharField(max_length=200, help_text="Ciudad o ubicación donde se encuentra la mascota")
    foto = models.ImageField(upload_to='mascotas/', blank=True, null=True)
    estado = models.CharField(max_length=15, choices=ESTADOS_MASCOTA, default='disponible')
    fecha_registro = models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='mascotas_registradas'
    )

    class Meta:
        verbose_name = "Mascota"
        verbose_name_plural = "Mascotas"
        ordering = ['-fecha_registro']

    def __str__(self):
        return f"{self.nombre} ({self.tipo})"


class SolicitudPublicacion(models.Model):
    """
    Solicitud de usuarios para publicar una mascota en adopción.
    Queda en 'pendiente' hasta que el admin la revise (parte 2).
    """
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='solicitudes_publicacion'
    )
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=10, choices=TIPOS_MASCOTA)
    raza = models.CharField(max_length=100)
    edad = models.PositiveIntegerField(help_text="Edad en meses")
    sexo = models.CharField(max_length=10, choices=SEXOS)
    descripcion = models.TextField()
    ubicacion = models.CharField(max_length=200)
    foto = models.ImageField(upload_to='mascotas/solicitudes/', blank=True, null=True)
    estado = models.CharField(max_length=15, default='pendiente')  # pendiente | aprobada | rechazada
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"SolicitudPublicacion({self.nombre}) de {self.usuario}"
