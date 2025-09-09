from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from registro_mascotas.models import Mascota
from portal_mascotas.constantes import ESTADOS_SOLICITUD

class SolicitudAdopcion(models.Model):
    """
    Solicitud de adopción de mascotas.
    
    Gestiona el proceso de solicitud de adopción, permitiendo a los usuarios
    solicitar adoptar una mascota específica y hacer seguimiento al estado
    de su solicitud (pendiente, aprobada, rechazada, cancelada).
    Utiliza las constantes definidas en portal_mascotas.constantes para los estados.
    """

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='solicitudes_adopcion')
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='solicitudes')
    mensaje = models.TextField(help_text="Motivo por el cual quieres adoptar esta mascota")
    estado = models.CharField(max_length=15, choices=ESTADOS_SOLICITUD, default='pendiente')
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    fecha_respuesta = models.DateTimeField(blank=True, null=True)
    respuesta = models.TextField(blank=True, help_text="Respuesta del responsable de la mascota")
    
    class Meta:
        verbose_name = "Solicitud de Adopción"
        verbose_name_plural = "Solicitudes de Adopción"
        ordering = ['-fecha_solicitud']
        unique_together = ['usuario', 'mascota']  # Un usuario no puede solicitar la misma mascota dos veces

    def clean(self):
        # Validar que la mascota esté disponible
        if self.mascota and self.mascota.estado != 'disponible':
            raise ValidationError('Esta mascota no está disponible para adopción.')
        
        # Validar que el usuario no sea el responsable de la mascota
        if self.usuario == self.mascota.responsable:
            raise ValidationError('No puedes solicitar adoptar tu propia mascota.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Solicitud de {self.usuario.username} para {self.mascota.nombre} - {self.get_estado_display()}"
