# portal_mascotas/urls.py
from django.contrib import admin
from django.urls import path, include
from portal_mascotas import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('accounts/', include(('login.urls', 'login'), namespace='login')),
    path('solicitudes/', include(('solicitud_adopcion.urls', 'solicitud_adopcion'), namespace='solicitud_adopcion')),
    path('blog/', include(('blog.urls', 'blog'), namespace='blog')),
]

# Servir media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
