from django import forms
from django.contrib import admin, messages
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from datetime import date
from .models import Mascota, SolicitudPublicacion


# ===================== Mascota =====================
@admin.register(Mascota)
class MascotaAdmin(admin.ModelAdmin):
    list_display = ("id", "thumb", "nombre", "tipo", "raza", "edad_meses_calc",
                    "sexo", "ubicacion", "estado", "responsable", "fecha_registro")
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
        ("Metadatos", {"classes": ("collapse",), "fields": ("fecha_registro",)}),
    )

    def edad_meses_calc(self, obj):
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


# ====== ActionForm (campo para motivo) ======
class RechazoActionForm(admin.helpers.ActionForm):
    rechazo_motivo = forms.CharField(
        label="Motivo del rechazo",
        required=False,
        widget=forms.Textarea(attrs={
            "rows": 3,
            "style": "width: 420px;",
            "placeholder": "Escribe el motivo del rechazo (obligatorio solo si vas a Rechazar)…"
        })
    )


# ===================== SolicitudPublicacion =====================
@admin.register(SolicitudPublicacion)
class SolicitudPublicacionAdmin(admin.ModelAdmin):
    list_display = ("id", "thumb", "nombre", "tipo", "raza", "edad", "sexo",
                    "ubicacion", "contacto_nombre", "contacto_email",
                    "estado", "usuario", "fecha_creacion")
    list_filter = ("estado", "tipo", "sexo", "fecha_creacion")
    search_fields = ("nombre", "raza", "ubicacion", "usuario__username",
                     "contacto_nombre", "contacto_email", "contacto_telefono")
    actions = ("accion_aceptar_publicacion", "accion_rechazar_publicacion")
    action_form = RechazoActionForm

    readonly_fields = (
        "usuario", "nombre", "tipo", "raza", "edad", "sexo",
        "descripcion", "ubicacion", "foto", "estado", "fecha_creacion",
        "contacto_nombre", "contacto_email", "contacto_direccion", "contacto_telefono",
        "acepta_declaracion",
        "rechazo_motivo", "aceptacion_mensaje",
        "preview",
    )

    def has_add_permission(self, request):
        return False  # Sin “Añadir” en esta tabla

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
        ("Datos de contacto del solicitante", {
            "fields": (
                ("contacto_nombre", "contacto_email"),
                ("contacto_telefono", "contacto_direccion"),
                "acepta_declaracion",
            )
        }),
        ("Revisión", {
            "fields": ("rechazo_motivo", "aceptacion_mensaje"),
        }),
    )

    # ---- Mini vistas de imagen ----
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

    # ---- Acciones ----
    @admin.action(description="Aceptar publicación (crear Mascota)")
    def accion_aceptar_publicacion(self, request, queryset):
        from .models import Mascota
        aprobadas = 0
        ya_procesadas = 0
        for s in queryset:
            if s.estado != "pendiente":
                ya_procesadas += 1
                continue
            Mascota.objects.create(
                nombre=s.nombre, tipo=s.tipo, raza=s.raza, edad=s.edad, sexo=s.sexo,
                descripcion=s.descripcion, ubicacion=s.ubicacion, foto=s.foto,
                estado="disponible", responsable=s.usuario
            )
            s.estado = "aprobada"
            s.aceptacion_mensaje = "✅ Tu solicitud fue aprobada. La mascota ya está publicada en el portal."
            s.save(update_fields=["estado", "aceptacion_mensaje"])
            aprobadas += 1

        if aprobadas:
            messages.success(
                request,
                f"✅ {aprobadas} solicitud(es) aceptada(s) y convertida(s) en Mascota."
            )
        if ya_procesadas:
            messages.warning(
                request,
                f"ℹ️ {ya_procesadas} solicitud(es) ya estaban procesadas."
            )

    @admin.action(description="Rechazar publicación (requiere motivo)")
    def accion_rechazar_publicacion(self, request, queryset):
        motivo = (request.POST.get("rechazo_motivo") or "").strip()
        if not motivo:
            messages.error(request, "Debes indicar el motivo del rechazo en el cuadro de texto antes de ejecutar la acción.")
            return

        rechazadas = 0
        for s in queryset:
            if s.estado == "pendiente":
                s.estado = "rechazada"
                s.rechazo_motivo = motivo
                s.save(update_fields=["estado", "rechazo_motivo"])
                rechazadas += 1

        if rechazadas:
            messages.success(request, f"🛑 {rechazadas} solicitud(es) rechazadas.")
        else:
            messages.info(request, "No había solicitudes 'pendientes' para rechazar.")

    # ---- Mostrar/ocultar textarea por acción (inyectado al final del body) ----
    def changelist_view(self, request, extra_context=None):
        resp = super().changelist_view(request, extra_context=extra_context)
        try:
            if hasattr(resp, "render") and callable(resp.render):
                resp.render()
            html = resp.content.decode("utf-8")

            js = """
<script>
(function(){
  function getNodes(){
    var sel   = document.getElementById('action');
    var ta    = document.querySelector('textarea[name="rechazo_motivo"]');
    var label = null;
    if(ta){
      var prev = ta.previousElementSibling;
      if(prev && prev.tagName && prev.tagName.toLowerCase()==='label'){ label = prev; }
      if(!label && ta.id){ label = document.querySelector('label[for="'+ta.id+'"]'); }
    }
    return { sel: sel, ta: ta, label: label };
  }
  function setVisible(show){
    var n = getNodes();
    if(!n.ta) return;
    n.ta.style.display    = show ? '' : 'none';
    if(n.label){ n.label.style.display = show ? '' : 'none'; }
  }
  function toggle(){
    var n = getNodes();
    if(!n.sel) return;
    setVisible(n.sel.value === 'accion_rechazar_publicacion');
  }
  document.addEventListener('DOMContentLoaded', function(){
    toggle(); // ✅ aplica el estado inicial según el valor actual del select
    var sel = document.getElementById('action');
    if(sel){ sel.addEventListener('change', toggle); }
  });
})();
</script>
"""
            resp.content = mark_safe(html.replace("</body>", js + "</body>"))
        except Exception:
            return resp
        return resp

