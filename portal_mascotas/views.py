# portal_mascotas/views.py

from django.db.models import Q
from django.db.models.functions import Lower
from django.shortcuts import render

from registro_mascotas.models import Mascota
from .constantes import TIPOS_MASCOTA, SEXOS, RANGOS_EDAD


def _rango_edad(edad_key: str):
    """
    Devuelve (min_meses, max_meses) a partir de la clave del rango.
    Espera que el parámetro `edad` sea el índice del rango como string.
    """
    if not edad_key:
        return None, None
    try:
        idx = int(edad_key)
        min_m, max_m, _label = RANGOS_EDAD[idx]
        return min_m, max_m
    except Exception:
        return None, None


def home(request):
    """
    Home público: lista de mascotas disponibles + filtros.
    Filtros: q (texto), tipo, ubic (ubicación), sexo, edad (índice de RANGOS_EDAD)
    """
    q = (request.GET.get("q") or "").strip()
    tipo = (request.GET.get("tipo") or "").strip()
    ubic = (request.GET.get("ubicacion") or "").strip()
    sexo = (request.GET.get("sexo") or "").strip()
    edad_key = (request.GET.get("edad") or "").strip()

    # Base queryset: solo disponibles
    qs = Mascota.objects.filter(estado="disponible")

    # Búsqueda por texto (ajusta campos según tu modelo)
    if q:
        qs = qs.filter(
            Q(nombre__icontains=q)
            | Q(descripcion__icontains=q)
            | Q(raza__icontains=q)
            | Q(ubicacion__icontains=q)
        )

    if tipo:
        qs = qs.filter(tipo=tipo)

    if ubic:
        qs = qs.filter(ubicacion__iexact=ubic)

    if sexo:
        qs = qs.filter(sexo=sexo)

    # Filtro por rango de edad (en meses)
    min_m, max_m = _rango_edad(edad_key)
    if min_m is not None and max_m is not None:
        qs = qs.filter(edad_meses__gte=min_m, edad_meses__lt=max_m)

    # Ubicaciones dinámicas (solo donde hay mascotas disponibles)
    ubicaciones = (
        Mascota.objects.filter(estado="disponible")
        .exclude(ubicacion__isnull=True)
        .exclude(ubicacion__exact="")
        .order_by(Lower("ubicacion"))
        .values_list("ubicacion", flat=True)
        .distinct()
    )

    ctx = {
        "mascotas": qs.order_by("-id"),
        "q": q,
        "tipo": tipo,
        "ubic": ubic,
        "sexo": sexo,
        "edad": edad_key,
        "tipos": TIPOS_MASCOTA,
        "sexos": SEXOS,
        "rangos_edad": RANGOS_EDAD,
        "ubicaciones": ubicaciones,
    }
    return render(request, "portal_mascotas/home.html", ctx)