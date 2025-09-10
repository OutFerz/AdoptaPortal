from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(BaseUserAdmin):
    """Admin para el modelo de usuario personalizado."""
    model = Usuario

    # Listado
    list_display = ("username", "email", "is_active", "is_staff", "is_superuser", "fecha_creacion")
    list_filter = ("is_active", "is_staff", "is_superuser", "groups")
    search_fields = ("username", "email")
    ordering = ("-fecha_creacion",)
    date_hierarchy = "fecha_creacion"

    # Campos de solo lectura (no editables en admin)
    readonly_fields = ("last_login", "date_joined", "fecha_creacion", "fecha_actualizacion")

    # ⚠️ Redefinimos todos los fieldsets para no duplicar campos
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Información personal", {"fields": ("first_name", "last_name", "email")}),
        (
            "Permisos",
            {
                "classes": ("collapse",),
                "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions"),
            },
        ),
        (
            "Fechas importantes",
            {
                "classes": ("collapse",),
                "fields": ("last_login", "date_joined", "fecha_creacion", "fecha_actualizacion"),
            },
        ),
    )

    # Form para crear usuarios desde admin
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )

    filter_horizontal = ("groups", "user_permissions")