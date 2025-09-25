from django.contrib import admin
from .models import SolicitudAdopcion

@admin.register(SolicitudAdopcion)
class SolicitudAdopcionAdmin(admin.ModelAdmin):
    list_display = ['id', 'usuario', 'mascota', 'estado', 'fecha_solicitud', 'fecha_respuesta']
    list_filter = ['estado', 'fecha_solicitud', 'mascota__tipo']
    search_fields = ['usuario__username', 'mascota__nombre', 'mensaje']
    readonly_fields = ['fecha_solicitud', 'fecha_respuesta']
    ordering = ['-fecha_solicitud']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('usuario', 'mascota', 'estado')
        }),
        ('Contenido', {
            'fields': ('mensaje', 'respuesta')
        }),
        ('Fechas', {
            'fields': ('fecha_solicitud', 'fecha_respuesta'),
            'classes': ('collapse',)
        }),
    )
