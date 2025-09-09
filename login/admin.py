from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    """
    Configuración del admin para el modelo Usuario personalizado
    """
    
    # Campos a mostrar en la lista
    list_display = ('username', 'email', 'is_active', 'fecha_creacion')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'fecha_creacion')
    search_fields = ('username', 'email')
    ordering = ('-fecha_creacion',)
    
    # Configuración de campos en el formulario
    fieldsets = (
        ('Información básica', {
            'fields': ('username', 'email', 'password')
        }),
        ('Permisos', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        ('Fechas importantes', {
            'fields': ('last_login', 'date_joined', 'fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
    
    # Campos para agregar nuevo usuario
    add_fieldsets = (
        ('Información básica', {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
    
    # Filtros en la barra lateral
    filter_horizontal = ('groups', 'user_permissions')
