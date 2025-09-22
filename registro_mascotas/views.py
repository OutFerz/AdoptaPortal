# registro_mascotas/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .forms import PublicarMascotaForm
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

    # 2) Si pidió el form pero no está logueado, lo mandamos a login y volvemos acá
    if not request.user.is_authenticated:
        return redirect(f"{reverse('login:login')}?next={request.get_full_path()}")

    # 3) Construcción del form
    form = PublicarMascotaForm(request.POST or None, request.FILES or None)

    # 4) Procesamiento
    if request.method == "POST" and form.is_valid():
        data = form.cleaned_data

        # Crear la solicitud
        SolicitudPublicacion.objects.create(
            usuario=request.user,
            # Datos de mascota
            nombre=data["nombre"],
            tipo=data["tipo"],
            raza=data["raza"],
            edad=data["edad"],
            sexo=data["sexo"],
            descripcion=data["descripcion"],
            ubicacion=data["ubicacion"],
            foto=data["foto"],
            # Datos de contacto
            contacto_nombre=data["contacto_nombre"],
            contacto_email=data["contacto_email"],
            contacto_direccion=data["contacto_direccion"],
            contacto_telefono=data["contacto_telefono"],
            # Seguridad / declaración
            acepta_declaracion=data["acepta_declaracion"],
        )

        messages.success(
            request,
            "✅ Solicitud enviada con éxito. Un administrador la revisará pronto."
        )
        return redirect("registro_mascotas:mis_solicitudes")

    # 5) Mostrar el formulario incrustado en home con bandera 'modo_publicar'
    return render(request, "portal_mascotas/home.html", {
        "modo_publicar": True,
        "form_publicar": form,
        "titulo_publicar": "Publicar mascota en adopción",
    })


@login_required
def mis_solicitudes(request):
    """
    Lista las solicitudes del usuario autenticado con su estado y mensajes
    (aceptada -> mensaje_aceptacion; rechazada -> motivo_rechazo).
    IMPORTANTE: el modelo debe tener el campo 'fecha_creacion'.
                Si en tu modelo se llama distinto (p.ej. 'created_at'),
                cambia el order_by por ese nombre.
    """
    qs = (SolicitudPublicacion.objects
          .filter(usuario=request.user)
          .order_by("-fecha_creacion"))  # <-- Cambia a "-created_at" si tu campo se llama así.

    return render(request, "registro_mascotas/mis_solicitudes.html", {
        "solicitudes": qs
    })

