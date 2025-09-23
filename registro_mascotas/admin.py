# registro_mascotas/admin.py
from django import forms
from django.contrib import admin, messages
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils import timezone
from django.http import HttpResponse
from datetime import date
import csv

from .models import Mascota, SolicitudPublicacion


# ===================== Mascota =====================
@admin.register(Mascota)
class MascotaAdmin(admin.ModelAdmin):
    list_display = (
        "id", "thumb", "nombre", "tipo", "raza", "edad_meses_calc",
        "sexo", "ubicacion", "estado", "responsable", "fecha_registro"
    )
    list_filter = ("estado", "tipo", "sexo", "ubicacion", "fecha_registro")
    search_fields = ("nombre", "raza", "ubicacion", "responsable__username", "descripcion")
    readonly_fields = ("fecha_registro", "preview")
    date_hierarchy = "fecha_registro"
    list_per_page = 25

    # Permite edición inline del estado sin entrar al objeto
    list_editable = ("estado",)
    # Asegura que el link al cambio quede en 'id' y 'nombre'
    list_display_links = ("id", "nombre")

    actions = (
        "accion_marcar_disponible",
        "accion_marcar_reservado",
        "accion_marcar_adoptado",
        "accion_exportar_csv",
    )

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

    # ---- Cálculo / vistas auxiliares ----
    @admin.display(description="Edad (meses)")
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

    @admin.display(description="Foto")
    def thumb(self, obj):
        if obj.foto:
            return format_html(
                '<img src="{}" style="height:48px;border-radius:6px;object-fit:cover" />',
                obj.foto.url,
            )
        return "—"

    @admin.display(description="Vista previa")
    def preview(self, obj):
        if obj.foto:
            return format_html(
                '<img src="{}" style="max-width:360px;border-radius:10px;" />',
                obj.foto.url,
            )
        return "—"

    # ---- Conveniencia: si no se especifica responsable, usar el usuario actual ----
    def save_model(self, request, obj, form, change):
        if not change and not getattr(obj, "responsable_id", None):
            obj.responsable = request.user
        super().save_model(request, obj, form, change)

    # ---- Acciones rápidas de estado ----
    @admin.action(description="Marcar como Disponible")
    def accion_marcar_disponible(self, request, queryset):
        updated = queryset.update(estado="disponible")
        if updated:
            messages.success(request, f"✅ {updated} mascota(s) marcadas como Disponible.")

    @admin.action(description="Marcar como Reservado")
    def accion_marcar_reservado(self, request, queryset):
        updated = queryset.update(estado="reservado")
        if updated:
            messages.success(request, f"⏳ {updated} mascota(s) marcadas como Reservado.")

    @admin.action(description="Marcar como Adoptado")
    def accion_marcar_adoptado(self, request, queryset):
        updated = queryset.update(estado="adoptado")
        if updated:
            messages.success(request, f"🎉 {updated} mascota(s) marcadas como Adoptado.")

    # ---- Exportar CSV ----
    @admin.action(description="Exportar selección a CSV")
    def accion_exportar_csv(self, request, queryset):
        now = timezone.now().strftime("%Y%m%d-%H%M%S")
        response = HttpResponse(content_type="text/csv; charset=utf-8")
        response["Content-Disposition"] = f'attachment; filename="mascotas-{now}.csv"'
        writer = csv.writer(response)
        writer.writerow([
            "id", "nombre", "tipo", "raza", "edad_meses", "sexo", "ubicacion",
            "estado", "responsable_username", "fecha_registro", "foto_path"
        ])
        for m in queryset:
            writer.writerow([
                m.id, m.nombre, m.get_tipo_display(), m.raza, getattr(m, "edad", ""),
                m.get_sexo_display(), m.ubicacion, m.get_estado_display(),
                getattr(m.responsable, "username", ""), m.fecha_registro.isoformat(),
                getattr(m.foto, "name", ""),
            ])
        return response


# ====== ActionForm (campo para motivo de rechazo) ======
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
    list_display = (
        "id", "thumb", "nombre", "tipo", "raza", "edad", "sexo",
        "ubicacion", "contacto_nombre", "contacto_email",
        "estado", "usuario", "fecha_creacion"
    )
    list_filter = ("estado", "tipo", "sexo", "fecha_creacion")
    search_fields = (
        "nombre", "raza", "ubicacion", "usuario__username",
        "contacto_nombre", "contacto_email", "contacto_telefono"
    )
    actions = ("accion_aceptar_publicacion", "accion_rechazar_publicacion")
    action_form = RechazoActionForm
    date_hierarchy = "fecha_creacion"
    list_per_page = 25

    readonly_fields = (
        "usuario", "nombre", "tipo", "raza", "edad", "sexo",
        "descripcion", "ubicacion", "foto", "estado", "fecha_creacion",
        "contacto_nombre", "contacto_email", "contacto_direccion", "contacto_telefono",
        "acepta_declaracion",
        "rechazo_motivo", "aceptacion_mensaje",
        "preview",
    )

    def has_add_permission(self, request):
        # Las solicitudes se crean desde el sitio público, no desde el admin
        return False

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
    @admin.display(description="Foto")
    def thumb(self, obj):
        if obj.foto:
            return format_html(
                '<img src="{}" style="height:48px;border-radius:6px;object-fit:cover" />',
                obj.foto.url,
            )
        return "—"

    @admin.display(description="Vista previa")
    def preview(self, obj):
        if obj.foto:
            return format_html(
                '<img src="{}" style="max-width:360px;border-radius:10px;" />',
                obj.foto.url,
            )
        return "—"

    # ---- Acciones ----
    @admin.action(description="Aceptar publicación (crear Mascota)")
    def accion_aceptar_publicacion(self, request, queryset):
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
            messages.success(request, f"✅ {aprobadas} solicitud(es) aceptada(s) y convertida(s) en Mascota.")
        if ya_procesadas:
            messages.warning(request, f"ℹ️ {ya_procesadas} solicitud(es) ya estaban procesadas.")

    @admin.action(description="Rechazar publicación (requiere motivo)")
    def accion_rechazar_publicacion(self, request, queryset):
        motivo = (request.POST.get("rechazo_motivo") or "").strip()
        if not motivo:
            messages.error(
                request,
                "Debes indicar el motivo del rechazo en el cuadro de texto antes de ejecutar la acción."
            )
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
    toggle(); // estado inicial
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