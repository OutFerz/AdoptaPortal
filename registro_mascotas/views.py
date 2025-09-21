# registro_mascotas/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import PublicarMascotaForm
from .models import SolicitudPublicacion

@login_required
def publicar_mascota(request):
    """
    Página para que el usuario envíe una solicitud de publicación de mascota.
    NO crea HTML nuevo: reutiliza 'portal_mascotas/home.html' activando un modo.
    - Si falta un campo: se muestra un mensaje claro.
    - Si todo OK: se guarda en estado 'pendiente' y se muestra confirmación.
    """
    if request.method == 'POST':
        form = PublicarMascotaForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            SolicitudPublicacion.objects.create(
                usuario=request.user,
                nombre=data['nombre'],
                tipo=data['tipo'],
                raza=data['raza'],
                edad=data['edad'],
                sexo=data['sexo'],
                descripcion=data['descripcion'],
                ubicacion=data['ubicacion'],
                foto=data.get('foto')  # puede venir vacío
            )
            messages.success(request, "✅ Solicitud enviada con éxito. Un administrador la revisará pronto.")
            return redirect('home')
        else:
            # Mostrar el primer error de forma simple
            for field, errs in form.errors.items():
                messages.error(request, f"Falta rellenar el campo: {form.fields[field].label}. {', '.join(errs)}")
                break
    else:
        form = PublicarMascotaForm()

    # Reutilizamos la página principal del portal
    return render(request, 'portal_mascotas/home.html', {
        'modo_publicar': True,
        'form_publicar': form,
        'titulo_publicar': 'Publicar mascota en adopción'
    })
