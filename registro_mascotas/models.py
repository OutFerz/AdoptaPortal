# registro_mascotas/models.py
from django.db import models
from django.conf import settings
from portal_mascotas.constantes import TIPOS_MASCOTA, SEXOS, ESTADOS_MASCOTA

class Mascota(models.Model):
    nombre = models.CharField(max_length=100, help_text="Nombre de la mascota")
    tipo = models.CharField(max_length=10, choices=TIPOS_MASCOTA)
    raza = models.CharField(max_length=100)
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
    Queda en 'pendiente' hasta que el admin la revise.
    """
    # Datos de la mascota
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

    # 👤 Datos de contacto del solicitante
    contacto_nombre = models.CharField(max_length=100, default='', blank=True)
    contacto_email = models.EmailField(default='', blank=True)
    contacto_direccion = models.CharField(max_length=200, default='', blank=True)
    contacto_telefono = models.CharField(max_length=30, default='', blank=True)

    # Seguridad / conformidad
    acepta_declaracion = models.BooleanField(default=False)

    # Flujo de revisión
    estado = models.CharField(max_length=15, default='pendiente')  # pendiente | aprobada | rechazada
    rechazo_motivo = models.TextField(default='', blank=True)      # motivo mostrado al usuario cuando se rechaza
    aceptacion_mensaje = models.TextField(default='', blank=True)  # mensaje automático al aprobar

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"SolicitudPublicacion({self.nombre}) de {self.usuario}"

