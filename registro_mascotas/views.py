# registro_mascotas/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .forms import SolicitudPublicacionForm
from .models import SolicitudPublicacion


def publicar_mascota(request):
    """
    Flujo:
      - GET sin ?modo -> muestra selector (dos tarjetas: Publicar / Ver estado)
      - GET con ?modo=form -> muestra el formulario (si no está logueado, redirige a login con next)
      - POST -> valida y crea la SolicitudPublicacion, luego redirige a 'mis_solicitudes'
    """
    modo = request.GET.get("modo")

    # 1) Selector simple si no pide el form directamente
    if modo != "form":
        return render(request, "portal_mascotas/home.html", {"modo_selector": True})

    # 2) Si pidió el form pero no está logueado, a login con next
    if not request.user.is_authenticated:
        return redirect(f"{reverse('login:login')}?next={request.get_full_path()}")

    # 3) Construcción del form
    if request.method == "POST":
        form = SolicitudPublicacionForm(request.POST, request.FILES)
        if form.is_valid():
            # 4) Guardar como pendiente asociando al usuario
            instancia: SolicitudPublicacion = form.save(commit=False)
            instancia.usuario = request.user
            # instancia.estado = "pendiente"  # el modelo ya tiene default, por si acaso
            instancia.save()

            messages.success(
                request,
                "✅ Solicitud enviada con éxito. Un administrador la revisará pronto."
            )
            return redirect("registro_mascotas:mis_solicitudes")
        else:
            messages.error(request, "Por favor corrige los errores del formulario.")
    else:
        # Prefill simple con datos del usuario
        initial = {
            "contacto_nombre": getattr(request.user, "username", "") or "",
            "contacto_email": getattr(request.user, "email", "") or "",
        }
        form = SolicitudPublicacionForm(initial=initial)

    # 5) Mostrar el formulario incrustado en home con bandera 'modo_publicar'
    return render(request, "portal_mascotas/home.html", {
        "modo_publicar": True,
        "form_publicar": form,
        "titulo_publicar": "Publicar mascota en adopción",
    })


@login_required
def mis_solicitudes(request):
    """
    Lista las solicitudes del usuario autenticado con su estado y mensajes.
    """
    qs = (
        SolicitudPublicacion.objects
        .filter(usuario=request.user)
        .order_by("-fecha_creacion")
    )
    return render(request, "registro_mascotas/mis_solicitudes.html", {"solicitudes": qs})