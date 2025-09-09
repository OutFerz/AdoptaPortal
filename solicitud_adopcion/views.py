from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import SolicitudAdopcion
from registro_mascotas.models import Mascota

@login_required
def lista_solicitudes(request):
    """Lista las solicitudes del usuario actual"""
    solicitudes = SolicitudAdopcion.objects.filter(usuario=request.user).order_by('-fecha_solicitud')
    context = {
        'solicitudes': solicitudes,
        'titulo': 'Mis Solicitudes de Adopción'
    }
    return render(request, 'solicitud_adopcion/lista_solicitudes.html', context)

@login_required
def crear_solicitud(request, mascota_id=None):
    """Crear una nueva solicitud de adopción"""
    if request.method == 'POST':
        # Lógica para crear solicitud
        mascota_id = request.POST.get('mascota_id')
        mensaje = request.POST.get('mensaje')
        
        if mascota_id and mensaje:
            try:
                mascota = Mascota.objects.get(id=mascota_id)
                solicitud = SolicitudAdopcion.objects.create(
                    usuario=request.user,
                    mascota=mascota,
                    mensaje=mensaje
                )
                messages.success(request, 'Solicitud enviada correctamente')
                return redirect('solicitud_adopcion:detalle_solicitud', solicitud.id)
            except Exception as e:
                messages.error(request, f'Error al crear solicitud: {str(e)}')
    
    # Si viene mascota_id, pre-seleccionar la mascota
    mascota = None
    if mascota_id:
        mascota = get_object_or_404(Mascota, id=mascota_id)
    
    mascotas_disponibles = Mascota.objects.filter(estado='disponible')
    context = {
        'mascota': mascota,
        'mascotas_disponibles': mascotas_disponibles,
        'titulo': 'Nueva Solicitud de Adopción'
    }
    return render(request, 'solicitud_adopcion/crear_solicitud.html', context)

@login_required
def detalle_solicitud(request, solicitud_id):
    """Ver detalles de una solicitud específica del usuario"""
    solicitud = get_object_or_404(SolicitudAdopcion, id=solicitud_id, usuario=request.user)
    context = {
        'solicitud': solicitud,
        'titulo': f'Mi Solicitud #{solicitud.id}'
    }
    return render(request, 'solicitud_adopcion/detalle_solicitud.html', context)

@login_required
def responder_solicitud(request, solicitud_id):
    """Responder a una solicitud de adopción (solo el responsable de la mascota)"""
    solicitud = get_object_or_404(SolicitudAdopcion, id=solicitud_id)
    
    # Verificar que el usuario es el responsable de la mascota
    if request.user != solicitud.mascota.responsable:
        messages.error(request, 'No tienes permisos para responder esta solicitud')
        return redirect('solicitud_adopcion:detalle_solicitud', solicitud_id)
    
    if request.method == 'POST':
        estado = request.POST.get('estado')
        respuesta = request.POST.get('respuesta', '')
        
        if estado in ['aprobada', 'rechazada']:
            solicitud.estado = estado
            solicitud.respuesta = respuesta
            solicitud.save()
            
            # Si se aprueba, cambiar estado de la mascota
            if estado == 'aprobada':
                solicitud.mascota.estado = 'adoptado'
                solicitud.mascota.save()
            
            messages.success(request, f'Solicitud {estado} correctamente')
            return redirect('solicitud_adopcion:detalle_solicitud', solicitud_id)
    
    context = {
        'solicitud': solicitud,
        'titulo': f'Responder Solicitud #{solicitud.id}'
    }
    return render(request, 'solicitud_adopcion/responder_solicitud.html', context)
