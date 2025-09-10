# registro_mascotas/admin.py
from django.contrib import admin
from .models import Mascota
from datetime import date

@admin.register(Mascota)
class MascotaAdmin(admin.ModelAdmin):
    """
    Mostramos una columna 'Edad (meses)' calculada que intenta usar:
    - obj.edad_meses (si existe),
    - o obj.edad (si tu campo se llama así y está en meses),
    - o calcula desde obj.fecha_nacimiento (si lo tienes como DateField).
    Así evitamos romper el admin si el nombre de campo cambió.
    """
    list_display = (
        "id",
        "nombre",
        "tipo",
        "sexo",
        "raza",
        "ubicacion",
        "edad_meses_calc",   # <— reemplaza 'edad_meses' por la versión calculada
        "estado",
    )
    list_filter = ("tipo", "sexo", "estado", "ubicacion")
    search_fields = ("nombre", "raza", "ubicacion")

    def edad_meses_calc(self, obj):
        # 1) Si existe un atributo/campo edad_meses, úsalo
        if hasattr(obj, "edad_meses") and getattr(obj, "edad_meses") is not None:
            return getattr(obj, "edad_meses")

        # 2) Si el campo se llama 'edad' y guardas meses, úsalo
        if hasattr(obj, "edad") and getattr(obj, "edad") is not None:
            return getattr(obj, "edad")

        # 3) Si tienes fecha_nacimiento, calcula meses
        if hasattr(obj, "fecha_nacimiento") and getattr(obj, "fecha_nacimiento"):
            fn = obj.fecha_nacimiento
            hoy = date.today()
            meses = (hoy.year - fn.year) * 12 + (hoy.month - fn.month)
            if hoy.day < fn.day:
                meses -= 1
            return max(meses, 0)

        # 4) Si nada aplica
        return "-"

    edad_meses_calc.short_description = "Edad (meses)"