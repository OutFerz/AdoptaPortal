from django.db import models
from django.conf import settings
from portal_mascotas.constantes import TIPOS_MASCOTA, SEXOS, ESTADOS_MASCOTA

class Mascota(models.Model):
    """
    Registro de mascotas disponibles para adopción.
    
    Este modelo almacena toda la información de las mascotas que están disponibles
    para adopción, incluyendo sus características físicas, ubicación y estado.
    Utiliza las constantes definidas en portal_mascotas.constantes para:
    - TIPOS_MASCOTA: tipos de mascotas (perro, gato, otro)
    - SEXOS: opciones de sexo (macho, hembra)
    - ESTADOS_MASCOTA: estados de disponibilidad (disponible, adoptado, reservado)
    """

    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=10, choices=TIPOS_MASCOTA)
    raza = models.CharField(max_length=100, blank=True)
    edad = models.PositiveIntegerField(help_text="Edad en meses")
    sexo = models.CharField(max_length=10, choices=SEXOS)
    descripcion = models.TextField(help_text="Descripción de la mascota")
    ubicacion = models.CharField(max_length=200, help_text="Ciudad o ubicación donde se encuentra la mascota")
    foto = models.ImageField(upload_to='mascotas/', blank=True, null=True)
    estado = models.CharField(max_length=15, choices=ESTADOS_MASCOTA, default='disponible')
    fecha_registro = models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mascotas_registradas')
    
    class Meta:
        verbose_name = "Mascota"
        verbose_name_plural = "Mascotas"
        ordering = ['-fecha_registro']
    
    def __str__(self):
        return f"{self.nombre} - {self.get_tipo_display()}"
    
    @classmethod
    def filtrar_por_especie(cls, tipo):
        """Filtrar mascotas por tipo de especie"""
        return cls.objects.filter(tipo=tipo, estado='disponible')
    
    @classmethod
    def filtrar_por_edad(cls, edad_min=None, edad_max=None):
        """Filtrar mascotas por rango de edad (en meses)"""
        queryset = cls.objects.filter(estado='disponible')
        if edad_min is not None:
            queryset = queryset.filter(edad__gte=edad_min)
        if edad_max is not None:
            queryset = queryset.filter(edad__lte=edad_max)
        return queryset
    
    @classmethod
    def filtrar_por_ubicacion(cls, ubicacion):
        """Filtrar mascotas por ubicación"""
        return cls.objects.filter(
            ubicacion__icontains=ubicacion, 
            estado='disponible'
        )
    
    @classmethod
    def filtrar_combinado(cls, tipo=None, edad_min=None, edad_max=None, ubicacion=None):
        """Filtrar mascotas con múltiples criterios"""
        queryset = cls.objects.filter(estado='disponible')
        
        if tipo:
            queryset = queryset.filter(tipo=tipo)
        if edad_min is not None:
            queryset = queryset.filter(edad__gte=edad_min)
        if edad_max is not None:
            queryset = queryset.filter(edad__lte=edad_max)
        if ubicacion:
            queryset = queryset.filter(ubicacion__icontains=ubicacion)
            
        return queryset
