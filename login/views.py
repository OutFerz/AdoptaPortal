# login/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .models import Usuario

def _resolve_next(request, fallback='home'):
    """
    Obtiene el 'next' desde POST o GET para redirigir correctamente
    después del login o acciones similares.
    """
    nxt = request.POST.get('next') or request.GET.get('next')
    return nxt if nxt else fallback

def login_view(request):
    """
    Login que acepta usuario o correo.
    - Intenta autenticar con lo que venga (por si el USERNAME_FIELD cambiara).
    - Si falla, busca por email (case-insensitive) y reintenta con el username real.
    """
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username_or_email = (request.POST.get('username') or '').strip()
        password = request.POST.get('password') or ''
        next_page = _resolve_next(request, 'home')

        if not username_or_email or not password:
            messages.error(request, "Por favor, completa todos los campos.")
            return render(request, 'login/login.html', {'titulo': 'Iniciar Sesión'})

        # 1) Intento directo (por si USERNAME_FIELD fuese 'email' o el usuario sí escribió su username)
        user = authenticate(request, username=username_or_email, password=password)

        # 2) Si no funcionó, intento por email de forma case-insensitive
        if user is None and '@' in username_or_email:
            # Buscar usuario(s) con ese email sin diferenciar mayúsculas/minúsculas
            qs = Usuario.objects.filter(email__iexact=username_or_email).order_by('-id')
            user_obj = qs.first()
            if user_obj:
                # Reautenticar usando el username real del modelo personalizado
                user = authenticate(request, username=user_obj.username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"¡Bienvenido, {user.username}!")
            return redirect(next_page)
        else:
            messages.error(request, "Usuario/Correo o contraseña inválidos.")

    # GET o POST fallido
    return render(request, 'login/login.html', {'titulo': 'Iniciar Sesión'})

def logout_view(request):
    """Cierre de sesión"""
    logout(request)
    messages.info(request, 'Has cerrado sesión correctamente')
    return redirect('login:login')

def register_view(request):
    """
    Registro simple.
    Nota: si tu modelo no tiene unique=True en email, podrías permitir duplicados.
    Este flujo ya avisa si existe otro usuario con el mismo correo/username.
    """
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = (request.POST.get('email') or '').strip()
        username = (request.POST.get('username') or '').strip()
        password1 = request.POST.get('password1') or ''
        password2 = request.POST.get('password2') or ''

        errors = []

        if not email:
            errors.append('El correo electrónico es obligatorio')
        elif Usuario.objects.filter(email__iexact=email).exists():
            errors.append('Este correo electrónico ya está registrado')

        if not username:
            errors.append('El nombre de usuario es obligatorio')
        elif Usuario.objects.filter(username__iexact=username).exists():
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
            for e in errors:
                messages.error(request, e)
        else:
            try:
                user = Usuario.objects.create_user(
                    username=username,
                    email=email,
                    password=password1
                )
                messages.success(request, f'¡Cuenta creada para {username}! Ya puedes iniciar sesión.')
                return redirect('login:login')
            except Exception:
                messages.error(request, 'Error al crear la cuenta. Inténtalo de nuevo.')

    return render(request, 'login/register.html', {'titulo': 'Registrarse'})

@login_required
def profile_view(request):
    """Perfil del usuario"""
    return render(request, 'login/profile.html', {
        'titulo': 'Mi Perfil',
        'usuario': request.user
    })
