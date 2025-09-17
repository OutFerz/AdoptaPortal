# portal_mascotas/views.py
from django.shortcuts import render
from django.db.models import Q
from registro_mascotas.models import Mascota
from portal_mascotas.constantes import TIPOS_MASCOTA, SEXOS, RANGOS_EDAD

def home(request):
    q    = (request.GET.get("q") or "").strip()
    tipo = (request.GET.get("tipo") or "").strip()
    sexo = (request.GET.get("sexo") or "").strip()
    edad = (request.GET.get("edad") or "").strip()   # índice del rango
    ubic = (request.GET.get("ubic") or "").strip()

    qs = Mascota.objects.filter(estado="disponible").order_by("-fecha_registro")

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
        qs = qs.filter(ubicacion__icontains=ubic)  # filtro de ubicación

    ctx = {
        "mascotas": qs,
        "tipos": TIPOS_MASCOTA,
        "sexos": SEXOS,
        "rangos_edad": RANGOS_EDAD,
        "q": q, "tipo": tipo, "sexo": sexo, "edad": edad, "ubic": ubic,
    }
    return render(request, "portal_mascotas/home.html", ctx)

