from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.urls import reverse
from .models import SolicitudAdopcion
from registro_mascotas.models import Mascota


@login_required
def lista_solicitudes(request):
    solicitudes = (
        SolicitudAdopcion.objects.filter(usuario=request.user)
        .order_by("-fecha_solicitud")
    )
    context = {"solicitudes": solicitudes, "titulo": "Mis Solicitudes"}
    return render(request, "solicitud_adopcion/lista_solicitudes.html", context)


@login_required
@require_POST
def crear_solicitud_rapida(request, mascota_id: int):
    mascota = get_object_or_404(Mascota, pk=mascota_id, estado="disponible")

    if mascota.responsable_id == request.user.id:
        messages.error(request, "No puedes solicitar adoptar tu propia mascota.")
        return redirect("home")

    mensaje = (request.POST.get("mensaje") or "").strip()

    try:
        ya_pendiente = SolicitudAdopcion.objects.filter(
            usuario=request.user, mascota=mascota, estado="pendiente"
        ).exists()

        if ya_pendiente:
            messages.info(request, f"Ya tienes una solicitud pendiente para {mascota.nombre}.")
        else:
            solicitud = SolicitudAdopcion.objects.create(
                usuario=request.user, mascota=mascota, mensaje=mensaje
            )
            print(f"🐾 Solicitud creada: id={solicitud.id} usuario={request.user.username} mascota={mascota.nombre}")
            messages.success(request, f"🐾 ¡Solicitud enviada con éxito para {mascota.nombre}! 🐾")
            return redirect(reverse("home") + "#flash")

    except ValidationError as e:
        messages.error(request, " ".join(getattr(e, "messages", [str(e)])))
    except IntegrityError:
        messages.info(request, f"Ya existe una solicitud vigente para {mascota.nombre}.")
    except Exception:
        messages.error(request, "No pudimos crear tu solicitud en este momento. Intenta nuevamente.")

    return redirect("home")


@login_required
def detalle_solicitud(request, solicitud_id: int):
    solicitud = get_object_or_404(SolicitudAdopcion, id=solicitud_id, usuario=request.user)
    context = {"solicitud": solicitud, "titulo": f"Mi Solicitud #{solicitud.id}"}
    return render(request, "solicitud_adopcion/detalle_solicitud.html", context)


@login_required
def responder_solicitud(request, solicitud_id: int):
    solicitud = get_object_or_404(SolicitudAdopcion, id=solicitud_id)

    if request.user != solicitud.mascota.responsable:
        messages.error(request, "No tienes permiso para responder esta solicitud.")
        return redirect("home")

    if request.method == "POST":
        estado = request.POST.get("estado")
        respuesta = (request.POST.get("respuesta") or "").strip()

        if estado in ["aprobada", "rechazada"]:
            solicitud.estado = estado
            solicitud.respuesta = respuesta
            solicitud.save()

            if estado == "aprobada":
                solicitud.mascota.estado = "adoptado"
                solicitud.mascota.save()

            messages.success(request, f"Solicitud {estado} correctamente.")
            return redirect("solicitud_adopcion:detalle_solicitud", solicitud_id)

    context = {"solicitud": solicitud, "titulo": f"Responder Solicitud #{solicitud.id}"}
    return render(request, "solicitud_adopcion/responder_solicitud.html", context)
