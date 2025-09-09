from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.urls import reverse
from .models import Usuario

def login_view(request):
    """Vista para el login de usuarios (con usuario o correo)"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username_or_email = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        
        if not username_or_email or not password:
            messages.error(request, "Por favor, completa todos los campos.")
        else:
            # Intentar autenticar primero con username
            user = authenticate(request, username=username_or_email, password=password)
            
            # Si no funciona, intentar con email
            if user is None:
                try:
                    # Buscar usuario por email
                    user_obj = Usuario.objects.get(email=username_or_email)
                    user = authenticate(request, username=user_obj.username, password=password)
                except Usuario.DoesNotExist:
                    user = None
            
            if user is not None:
                login(request, user)
                messages.success(request, f"¡Bienvenido, {user.username}!")
                # Redirigir a la página que intentaba acceder o al dashboard
                next_page = request.GET.get('next', 'dashboard')
                return redirect(next_page)
            else:
                messages.error(request, "Usuario/Correo o contraseña inválidos.")
    
    return render(request, 'login/login.html', {
        'titulo': 'Iniciar Sesión'
    })

def logout_view(request):
    """Vista para cerrar sesión"""
    logout(request)
    messages.info(request, 'Has cerrado sesión correctamente')
    return redirect('login:login')

def register_view(request):
    """Vista para el registro de nuevos usuarios"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        # Obtener datos del formulario
        email = request.POST.get('email', '').strip()
        username = request.POST.get('username', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        
        # Validaciones básicas
        errors = []
        
        if not email:
            errors.append('El correo electrónico es obligatorio')
        elif Usuario.objects.filter(email=email).exists():
            errors.append('Este correo electrónico ya está registrado')
        if not username:
            errors.append('El nombre de usuario es obligatorio')
        elif Usuario.objects.filter(username=username).exists():
            errors.append('Este nombre de usuario ya está en uso')
        if not password1:
            errors.append('La contraseña es obligatoria')
        elif len(password1) < 8:
            errors.append('La contraseña debe tener al menos 8 caracteres')
        if not password2:
            errors.append('Debes confirmar la contraseña')
        elif password1 != password2:
            errors.append('Las contraseñas no coinciden')
        
        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            try:
                # Crear usuario usando el modelo personalizado
                user = Usuario.objects.create_user(
                    username=username,
                    email=email,
                    password=password1
                )
                messages.success(request, f'¡Cuenta creada para {username}! Ya puedes iniciar sesión.')
                return redirect('login:login')
            except Exception as e:
                messages.error(request, 'Error al crear la cuenta. Inténtalo de nuevo.')
    
    return render(request, 'login/register.html', {
        'titulo': 'Registrarse'
    })

@login_required
def profile_view(request):
    """Vista del perfil del usuario"""
    return render(request, 'login/profile.html', {
        'titulo': 'Mi Perfil',
        'usuario': request.user
    })