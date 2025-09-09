from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    """Dashboard principal del usuario"""
    context = {
        'titulo': 'Mi Sitio Mascota',
        'usuario': request.user
    }
    return render(request, 'portal_mascotas/dashboard.html', context)