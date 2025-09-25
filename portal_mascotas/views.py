# portal_mascotas/views.py
from django.shortcuts import render
from django.db.models import Q
from django.db.models.functions import Lower
from registro_mascotas.models import Mascota
from portal_mascotas.constantes import (
    TIPOS_MASCOTA, SEXOS, RANGOS_EDAD, REGIONES_CIUDADES
)

# --- Soporte opcional para búsqueda sin tildes en PostgreSQL ---
try:
    # Requiere: CREATE EXTENSION IF NOT EXISTS unaccent;
    from django.contrib.postgres.functions import Unaccent
    HAS_UNACCENT = True
except Exception:
    HAS_UNACCENT = False

import unicodedata


def _unaccent_py(s: str) -> str:
    """Quita tildes en Python (para construir patrón si no hay Unaccent)."""
    s = s or ""
    return "".join(
        c for c in unicodedata.normalize("NFKD", s)
        if not unicodedata.combining(c)
    )


def home(request):
    q     = (request.GET.get("q") or "").strip()
    tipo  = (request.GET.get("tipo") or "").strip()
    sexo  = (request.GET.get("sexo") or "").strip()
    edad  = (request.GET.get("edad") or "").strip()   # índice del rango
    ubic  = (request.GET.get("ubic") or "").strip()   # compatibilidad previa (puede venir vacío)

    # nuevos
    region = (request.GET.get("region") or "").strip()
    ciudad = (request.GET.get("ciudad") or "").strip()

    qs = Mascota.objects.filter(estado="disponible").order_by("-fecha_registro")

    # ===== Texto libre =====
    if q:
        qs = qs.filter(
            Q(nombre__icontains=q) |
            Q(raza__icontains=q) |
            Q(descripcion__icontains=q)
        )

    if tipo:
        qs = qs.filter(tipo=tipo)

    if sexo:
        qs = qs.filter(sexo=sexo)

    if edad != "":
        try:
            idx = int(edad)
            min_m, max_m, _ = RANGOS_EDAD[idx]
            qs = qs.filter(edad__gte=min_m, edad__lte=max_m)  # campo correcto: 'edad'
        except (ValueError, IndexError):
            pass

    if ubic:
        # filtro de ubicación previo (no se rompe)
        qs = qs.filter(ubicacion__icontains=ubic)

    # ===== región / ciudad - filtro menos estricto =====
    has_region_field = any(f.name == "region" for f in Mascota._meta.fields)
    has_ciudad_field = any(f.name == "ciudad" for f in Mascota._meta.fields)
    has_ubic_field   = any(f.name == "ubicacion" for f in Mascota._meta.fields)

    # Anotaciones una sola vez para usar Unaccent+Lower en varios filtros (si procede)
    annotations = {}
    if HAS_UNACCENT:
        if has_region_field:
            annotations["region_norm"] = Unaccent(Lower("region"))
        if has_ciudad_field:
            annotations["ciudad_norm"] = Unaccent(Lower("ciudad"))
        if has_ubic_field:
            annotations["ubicacion_norm"] = Unaccent(Lower("ubicacion"))

    if annotations:
        qs = qs.annotate(**annotations)

    def contains_expr(field: str, value: str):
        """Devuelve kwargs para __contains (con alias *_norm) o __icontains normal."""
        if not value:
            return {}
        if HAS_UNACCENT and f"{field}_norm" in annotations:
            return {f"{field}_norm__contains": _unaccent_py(value).lower()}
        else:
            # sin unaccent -> al menos case-insensitive
            return {f"{field}__icontains": value}

    # Filtro por ciudad (si el usuario la eligió)
    if ciudad:
        if has_ciudad_field:
            qs = qs.filter(**contains_expr("ciudad", ciudad))
        elif has_ubic_field:
            qs = qs.filter(**contains_expr("ubicacion", ciudad))

    # Filtro por región (directo + por ciudades de esa región si no hay ciudad seleccionada)
    if region:
        region_q = Q()
        if has_region_field:
            region_q |= Q(**contains_expr("region", region))

        if not ciudad:
            ciudades_region = REGIONES_CIUDADES.get(region, [])
            norm_cities = [_unaccent_py(c).lower() for c in ciudades_region] if HAS_UNACCENT else ciudades_region

            if has_ciudad_field or has_ubic_field:
                city_q = Q()
                for i, c in enumerate(norm_cities):
                    if not c:
                        continue
                    if has_ciudad_field:
                        if HAS_UNACCENT and "ciudad_norm" in annotations:
                            city_q |= Q(ciudad_norm__contains=c)
                        else:
                            city_q |= Q(ciudad__icontains=ciudades_region[i])
                    if has_ubic_field:
                        if HAS_UNACCENT and "ubicacion_norm" in annotations:
                            city_q |= Q(ubicacion_norm__contains=c)
                        else:
                            city_q |= Q(ubicacion__icontains=ciudades_region[i])
                region_q |= city_q

        qs = qs.filter(region_q)

    # ===== listas para selects =====
    regiones_disponibles = list(REGIONES_CIUDADES.keys())
    ciudades_disponibles = REGIONES_CIUDADES.get(region, []) if region else []

    ctx = {
        "mascotas": qs,
        "tipos": TIPOS_MASCOTA,
        "sexos": SEXOS,
        "rangos_edad": RANGOS_EDAD,

        "q": q, "tipo": tipo, "sexo": sexo, "edad": edad, "ubic": ubic,

        "region": region,
        "ciudad": ciudad,
        "regiones": regiones_disponibles,
        "ciudades": ciudades_disponibles,

        # Para JS en el template (dependiente sin recargar):
        "REGIONES_CIUDADES": REGIONES_CIUDADES,
    }
    return render(request, "portal_mascotas/home.html", ctx)
