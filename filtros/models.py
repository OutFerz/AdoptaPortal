from django.db import models
from django.conf import settings
from registro_mascotas.models import Mascota
from portal_mascotas.constantes import TIPOS_MASCOTA, SEXOS

class FiltroBusqueda(models.Model):
    """
    Filtros por especie, edad, ubicación y otros criterios.
    
    Permite a los usuarios guardar y reutilizar filtros de búsqueda personalizados
    para encontrar mascotas que cumplan con criterios específicos como tipo,
    edad, ubicación, raza, etc.
    Utiliza las constantes definidas en portal_mascotas.constantes para:
    - TIPOS_MASCOTA: tipos de mascotas (perro, gato, otro)
    - SEXOS: opciones de sexo (macho, hembra)
    """
    
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='filtros_busqueda', null=True, blank=True)
    nombre_filtro = models.CharField(max_length=100, help_text="Nombre para identificar este filtro")
    
    # Filtros por características
    tipo = models.CharField(max_length=10, choices=TIPOS_MASCOTA, blank=True, null=True)
    sexo = models.CharField(max_length=10, choices=SEXOS, blank=True, null=True)
    edad_min = models.PositiveIntegerField(blank=True, null=True, help_text="Edad mínima en meses")
    edad_max = models.PositiveIntegerField(blank=True, null=True, help_text="Edad máxima en meses")
    ubicacion = models.CharField(max_length=200, blank=True, help_text="Ciudad o ubicación")
    
    # Filtros adicionales
    raza = models.CharField(max_length=100, blank=True, help_text="Raza específica")
    incluir_descripcion = models.BooleanField(default=False, help_text="Incluir búsqueda en descripción")
    texto_busqueda = models.CharField(max_length=200, blank=True, help_text="Texto a buscar en nombre o descripción")
    
    # Metadatos
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_ultimo_uso = models.DateTimeField(auto_now=True)
    es_favorito = models.BooleanField(default=False, help_text="Marcar como filtro favorito")
    
    class Meta:
        verbose_name = "Filtro de Búsqueda"
        verbose_name_plural = "Filtros de Búsqueda"
        ordering = ['-fecha_ultimo_uso']
    
    def aplicar_filtro(self):
        """Aplicar este filtro y devolver las mascotas que coinciden"""
        queryset = Mascota.objects.filter(estado='disponible')
        
        if self.tipo:
            queryset = queryset.filter(tipo=self.tipo)
        if self.sexo:
            queryset = queryset.filter(sexo=self.sexo)
        if self.edad_min is not None:
            queryset = queryset.filter(edad__gte=self.edad_min)
        if self.edad_max is not None:
            queryset = queryset.filter(edad__lte=self.edad_max)
        if self.ubicacion:
            queryset = queryset.filter(ubicacion__icontains=self.ubicacion)
        if self.raza:
            queryset = queryset.filter(raza__icontains=self.raza)
        if self.texto_busqueda:
            if self.incluir_descripcion:
                queryset = queryset.filter(
                    models.Q(nombre__icontains=self.texto_busqueda) |
                    models.Q(descripcion__icontains=self.texto_busqueda)
                )
            else:
                queryset = queryset.filter(nombre__icontains=self.texto_busqueda)
        
        return queryset
    
    def get_criterios_activos(self):
        """Obtener una lista de los criterios de filtro que están activos"""
        criterios = []
        if self.tipo:
            criterios.append(f"Especie: {self.get_tipo_display()}")
        if self.sexo:
            criterios.append(f"Sexo: {self.get_sexo_display()}")
        if self.edad_min or self.edad_max:
            edad_str = "Edad: "
            if self.edad_min and self.edad_max:
                edad_str += f"{self.edad_min}-{self.edad_max} meses"
            elif self.edad_min:
                edad_str += f"más de {self.edad_min} meses"
            elif self.edad_max:
                edad_str += f"menos de {self.edad_max} meses"
            criterios.append(edad_str)
        if self.ubicacion:
            criterios.append(f"Ubicación: {self.ubicacion}")
        if self.raza:
            criterios.append(f"Raza: {self.raza}")
        if self.texto_busqueda:
            criterios.append(f"Búsqueda: {self.texto_busqueda}")
        
        return criterios
    
    def __str__(self):
        if self.nombre_filtro:
            return self.nombre_filtro
        criterios = self.get_criterios_activos()
        if criterios:
            return " | ".join(criterios[:2])  # Mostrar máximo 2 criterios
        return f"Filtro #{self.id}"

class HistorialBusqueda(models.Model):
    """Modelo para guardar el historial de búsquedas realizadas"""
    
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='historial_busquedas')
    filtro_aplicado = models.ForeignKey(FiltroBusqueda, on_delete=models.CASCADE, null=True, blank=True)
    criterios_busqueda = models.JSONField(help_text="Criterios de búsqueda aplicados")
    resultados_encontrados = models.PositiveIntegerField(default=0)
    fecha_busqueda = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Historial de Búsqueda"
        verbose_name_plural = "Historial de Búsquedas"
        ordering = ['-fecha_busqueda']
    
    def __str__(self):
        return f"Búsqueda de {self.usuario.username} - {self.fecha_busqueda.strftime('%d/%m/%Y %H:%M')}"
