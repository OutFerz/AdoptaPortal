# registro_mascotas/admin.py
from django.contrib import admin, messages
from django.utils.html import format_html
from datetime import date

from .models import Mascota, SolicitudPublicacion


# =========================
#  ADMIN: Mascota
# =========================
@admin.register(Mascota)
class MascotaAdmin(admin.ModelAdmin):
    list_display = (
        "id", "thumb", "nombre", "tipo", "raza", "edad_meses_calc",
        "sexo", "ubicacion", "estado", "responsable", "fecha_registro"
    )
    list_filter = ("estado", "tipo", "sexo", "ubicacion", "fecha_registro")
    search_fields = ("nombre", "raza", "ubicacion", "responsable__username")
    readonly_fields = ("fecha_registro", "preview")

    fieldsets = (
        ("Datos de la mascota", {
            "fields": (
                ("nombre", "tipo", "sexo"),
                ("raza", "edad"),
                "descripcion",
                ("ubicacion", "estado"),
                ("foto", "preview"),
                "responsable",
            )
        }),
        ("Metadatos", {
            "classes": ("collapse",),
            "fields": ("fecha_registro",)
        }),
    )

    def edad_meses_calc(self, obj):
        """Muestra la edad en meses aunque cambie el campo en el modelo."""
        if hasattr(obj, "edad") and isinstance(obj.edad, int):
            return obj.edad
        if hasattr(obj, "edad_meses") and isinstance(obj.edad_meses, int):
            return obj.edad_meses
        if hasattr(obj, "fecha_nacimiento") and isinstance(obj.fecha_nacimiento, date):
            hoy = date.today()
            meses = (hoy.year - obj.fecha_nacimiento.year) * 12 + (hoy.month - obj.fecha_nacimiento.month)
            return max(meses, 0)
        return "-"

    edad_meses_calc.short_description = "Edad (meses)"

    def thumb(self, obj):
        if obj.foto:
            return format_html('<img src="{}" style="height:48px;border-radius:6px;object-fit:cover" />', obj.foto.url)
        return "—"
    thumb.short_description = "Foto"

    def preview(self, obj):
        if obj.foto:
            return format_html('<img src="{}" style="max-width:360px;border-radius:10px;" />', obj.foto.url)
        return "—"
    preview.short_description = "Vista previa"


# =========================
#  ADMIN: SolicitudPublicacion
# =========================
@admin.register(SolicitudPublicacion)
class SolicitudPublicacionAdmin(admin.ModelAdmin):
    list_display = (
        "id", "thumb", "nombre", "tipo", "raza", "edad",
        "sexo", "ubicacion", "estado", "usuario", "fecha_creacion"
    )
    list_filter = ("estado", "tipo", "sexo", "fecha_creacion")
    search_fields = ("nombre", "raza", "ubicacion", "usuario__username")
    actions = ("accion_aceptar_publicacion", "accion_rechazar_publicacion")
    readonly_fields = (
        "usuario", "nombre", "tipo", "raza", "edad", "sexo",
        "descripcion", "ubicacion", "foto", "estado", "fecha_creacion",
        "preview"
    )

    fieldsets = (
        ("Solicitud enviada por el usuario", {
            "fields": (
                ("usuario", "estado"),
                ("nombre", "tipo", "sexo"),
                ("raza", "edad"),
                "descripcion",
                ("ubicacion",),
                ("foto", "preview"),
                ("fecha_creacion",),
            )
        }),
    )

    # ---------- Vistas de imagen ----------
    def thumb(self, obj):
        if obj.foto:
            return format_html('<img src="{}" style="height:48px;border-radius:6px;object-fit:cover" />', obj.foto.url)
        return "—"
    thumb.short_description = "Foto"

    def preview(self, obj):
        if obj.foto:
            return format_html('<img src="{}" style="max-width:360px;border-radius:10px;" />', obj.foto.url)
        return "—"
    preview.short_description = "Vista previa"

    # ---------- Acciones ----------
    @admin.action(description="Aceptar publicación (crear Mascota)")
    def accion_aceptar_publicacion(self, request, queryset):
        """
        Crea una Mascota con los datos de la solicitud y marca la solicitud como 'aprobada'.
        - estado de la Mascota: 'disponible'
        - responsable: el usuario que envió la solicitud (puedes cambiarlo a request.user si prefieres)
        """
        aprobadas = 0
        ya_procesadas = 0

        for s in queryset:
            if s.estado != "pendiente":
                ya_procesadas += 1
                continue

            mascota = Mascota.objects.create(
                nombre=s.nombre,
                tipo=s.tipo,
                raza=s.raza,
                edad=s.edad,
                sexo=s.sexo,
                descripcion=s.descripcion,
                ubicacion=s.ubicacion,
                foto=s.foto,                   # reutiliza el archivo subido
                estado="disponible",
                responsable=s.usuario,         # o usa: request.user
            )
            s.estado = "aprobada"
            s.save(update_fields=["estado"])
            aprobadas += 1

        if aprobadas:
            messages.success(request, f"✅ {aprobadas} solicitud(es) aceptada(s) y convertida(s) en Mascota.")
        if ya_procesadas:
            messages.warning(request, f"ℹ️ {ya_procesadas} solicitud(es) ya estaban procesadas (no 'pendiente').")

    @admin.action(description="Rechazar publicación")
    def accion_rechazar_publicacion(self, request, queryset):
        rechazadas = 0
        for s in queryset:
            if s.estado == "pendiente":
                s.estado = "rechazada"
                s.save(update_fields=["estado"])
                rechazadas += 1
        if rechazadas:
            messages.success(request, f"🛑 {rechazadas} solicitud(es) marcadas como rechazadas.")
        else:
            messages.info(request, "No había solicitudes 'pendientes' para rechazar.")

