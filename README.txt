# Portal de Mascotas 🐾🐾

Un portal web desarrollado en Django para la gestión y adopción de mascotas.

## 📋 Descripción

Portal de Mascotas es una aplicación web que permite:
- **Gestión de mascotas**: Registro y administración de información de mascotas
- **Sistema de adopciones**: Proceso completo de adopción de mascotas
- **Filtros avanzados**: Búsqueda y filtrado de mascotas por diferentes criterios
- **Blog**: Artículos y noticias relacionadas con el cuidado de mascotas

## 🛠️ Tecnologías Utilizadas

- **Backend**: Django 5.2.6
- **Base de datos**: SQLite (desarrollo)
- **Frontend**: HTML, CSS, JavaScript
- **Python**: 3.11+
- **Arquitectura**: Modelo-Vista-Template (MVT)
- **ORM**: Django ORM con relaciones complejas
- **Validaciones**: Validaciones automáticas en modelos
- **Sistema de constantes**: Centralización de opciones compartidas

### ✨ Características Principales

- **🔍 Sistema de Filtros Inteligente**: Búsqueda avanzada con múltiples criterios
- **💾 Filtros Guardados**: Los usuarios pueden guardar y reutilizar filtros personalizados
- **📊 Historial de Búsquedas**: Registro completo de todas las búsquedas realizadas
- **✅ Validaciones Automáticas**: Prevención de solicitudes duplicadas o inválidas
- **🎯 Constantes Centralizadas**: Sistema sin duplicación de datos
- **🔗 Relaciones Complejas**: Modelos interconectados con integridad referencial
- **📱 Interfaz Intuitiva**: Diseño centrado en la experiencia del usuario

## 📦 Dependencias y Instalación Rápida

### 📋 Archivo requirements.txt
El proyecto incluye un archivo `requirements.txt` con todas las dependencias necesarias:

```
Django==5.2.6    Es: Framework web principal para crear aplicaciones
asgiref==3.9.1   Es: Librería para comunicación asíncrona y WebSockets
sqlparse==0.5.3  Es: Parser SQL para interpretar consultas de base de datos
tzdata==2025.2   Es: Base de datos de zonas horarias mundiales
Pillow==11.3.0   Es: Librería para procesamiento de imágenes (ImageField)
```

### 📝 ¿Cómo usar requirements.txt?

**Para instalar dependencias:**
```bash
pip install -r requirements.txt
```

**Para generar requirements.txt (después de instalar nuevas librerías):**
```bash
pip freeze > requirements.txt
```

**Para ver dependencias instaladas:**
```bash
pip list
```

**Para desinstalar todas las dependencias:**
```bash
pip uninstall -r requirements.txt -y
```

### 🚀 Instalación Rápida (4 pasos)

1. **Obtener el proyecto** (ver paso 2.1 de la instalación completa)
   ```bash
   # Opción A: Clonar con Git
   git clone https://github.com/Tornadusk/PortalMascotas.git
   cd PortalMascotas
   
   # Opción B: Descargar desde https://github.com/Tornadusk/PortalMascotas
   ```

2. **Activar el entorno virtual** (ver paso 2.2 de la instalación completa)
   ```bash
   # Linux/Mac
   source venv/bin/activate
   
   # Windows
   venv\Scripts\activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verificar instalación**
   ```bash
   python manage.py check
   ```

## 🚀 Instalación Completa

### 1. Prerrequisitos

**1.1. Instalar Python**
- Descargar desde: https://python.org
- Versión recomendada: Python 3.11 o superior
- ✅ Marcar "Add Python to PATH" durante la instalación
- Verificar instalación: `python --version`

**1.2. Verificar pip**
- pip se instala automáticamente con Python
- Verificar: `pip --version`

**1.3. Instalar Git**
- Descargar desde: https://git-scm.com
- Verificar: `git --version`

### 2. Pasos de Instalación

**2.1. Obtener el proyecto**

**Opción A: Clonar con Git (recomendado)**
   ```bash
   git clone https://github.com/Tornadusk/PortalMascotas.git
   cd PortalMascotas
   ```

**Opción B: Descargar desde GitHub**
   - Ir a: https://github.com/Tornadusk/PortalMascotas
   - Hacer clic en "Code" → "Download ZIP"
   - Extraer el archivo ZIP
   - Abrir terminal en la carpeta extraída

**2.2. Crear y activar entorno virtual**
   ```bash
   # Crear entorno virtual
   python -m venv venv
   
   # Activar (Linux/Mac)
   source venv/bin/activate
   
   # Activar (Windows)
   venv\Scripts\activate
   ```

**2.3. Instalar dependencias**

**Opción A: Instalar todas las dependencias (recomendado)**
   ```bash
   # Instalar todas las dependencias del proyecto
   pip install -r requirements.txt
   
   # Verificar que se instalaron correctamente
   pip list
   ```

**Opción B: Instalar Django manualmente**
   ```bash
   # Instalar solo Django (instala dependencias automáticamente)
   pip install django
   
   # Verificar instalación
   python -m django --version
   ```

**2.4. Configurar base de datos**
   ```bash
   python manage.py migrate
   ```

**2.5. Crear superusuario (opcional)**
   ```bash
   python manage.py createsuperuser
   ```

**2.6. Ejecutar servidor**
   ```bash
   python manage.py runserver
   ```

**2.7. Acceder a la aplicación**
   - URL: `http://127.0.0.1:8000/`
   - Admin: `http://127.0.0.1:8000/admin/`

## 🏗️ Estructura del Proyecto

```
PortalMascotas/
├── registro_mascotas/     # App para registro de mascotas
├── solicitud_adopcion/    # App para solicitudes de adopción
├── filtros/               # App para filtros y búsquedas
├── blog/                  # App para blog y artículos
├── portal_mascotas/       # Configuración del proyecto
│   ├── settings.py        # Configuraciones
│   ├── urls.py            # URLs principales
│   └── wsgi.py            # Configuración WSGI
└── manage.py              # Script de administración de Django
```

## 🚀 Comandos Útiles

### Desarrollo
```bash
# Ejecutar servidor de desarrollo
python manage.py runserver

# Verificar configuración
python manage.py check

# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# ⚠️ SOLUCIÓN DE ERRORES DE MIGRACIONES
# Si obtienes error "InconsistentMigrationHistory" al crear migraciones:
# 1. Eliminar la base de datos
del db.sqlite3

# 2. Crear migraciones nuevamente
python manage.py makemigrations

# 3. Aplicar migraciones
python manage.py migrate

# 4. Crear superusuario
python manage.py createsuperuser

# 📝 NOTA: Si solo se crean migraciones para algunas apps:
# Crear migraciones para todas las apps específicamente:
python manage.py makemigrations registro_mascotas
python manage.py makemigrations solicitud_adopcion
python manage.py makemigrations filtros
python manage.py makemigrations login
python manage.py makemigrations blog

# Luego aplicar todas las migraciones:
python manage.py migrate
```

### Administración
```bash
# Ejecutar servidor y acceder al admin
python manage.py runserver
# Luego ir a: http://127.0.0.1:8000/admin/

# Crear superusuario
python manage.py createsuperuser
```

## 🏗️ Arquitectura del Sistema

### 📊 Modelos de Datos

#### 🐕 Modelo Mascota (`registro_mascotas`)
```python
# Campos principales
- nombre: Nombre de la mascota
- tipo: Especie (perro, gato, otro)
- raza: Raza específica
- edad: Edad en meses
- sexo: Macho o hembra
- descripcion: Descripción detallada
- ubicacion: Ciudad o ubicación
- foto: Imagen de la mascota
- estado: Disponible, adoptado, reservado
- responsable: Usuario que registró la mascota
- fecha_registro: Fecha de registro

# Métodos de filtrado
- filtrar_por_especie(tipo)
- filtrar_por_edad(edad_min, edad_max)
- filtrar_por_ubicacion(ubicacion)
- filtrar_combinado(tipo, edad_min, edad_max, ubicacion)
```

#### 🏠 Modelo SolicitudAdopcion (`solicitud_adopcion`)
```python
# Campos principales
- usuario: Usuario que solicita la adopción
- mascota: Mascota a adoptar
- mensaje: Motivo de la adopción
- estado: Pendiente, aprobada, rechazada, cancelada
- fecha_solicitud: Fecha de la solicitud
- fecha_respuesta: Fecha de respuesta
- respuesta: Respuesta del responsable

# Validaciones automáticas
- Un usuario no puede solicitar la misma mascota dos veces
- Solo mascotas disponibles pueden ser solicitadas
- Un usuario no puede solicitar adoptar su propia mascota
```

#### 🔍 Modelo FiltroBusqueda (`filtros`)
```python
# Filtros disponibles
- tipo: Especie de mascota
- sexo: Sexo de la mascota
- edad_min/edad_max: Rango de edad
- ubicacion: Ubicación geográfica
- raza: Raza específica
- texto_busqueda: Búsqueda de texto
- incluir_descripcion: Incluir descripción en búsqueda

# Funcionalidades
- aplicar_filtro(): Ejecuta la búsqueda
- get_criterios_activos(): Muestra filtros aplicados
- Filtros favoritos y guardados
- Historial de búsquedas
```

### 🎯 Sistema de Constantes Centralizadas

El proyecto utiliza un sistema de constantes centralizadas en `portal_mascotas/constantes.py` para evitar duplicación de datos:

```python
# Tipos de mascotas
TIPOS_MASCOTA = [('perro', 'Perro'), ('gato', 'Gato'), ('otro', 'Otro')]

# Sexos
SEXOS = [('macho', 'Macho'), ('hembra', 'Hembra')]

# Estados de mascotas
ESTADOS_MASCOTA = [('disponible', 'Disponible'), ('adoptado', 'Adoptado'), ('reservado', 'Reservado')]

# Estados de solicitudes
ESTADOS_SOLICITUD = [('pendiente', 'Pendiente'), ('aprobada', 'Aprobada'), ('rechazada', 'Rechazada'), ('cancelada', 'Cancelada')]

# Rangos de edad comunes
RANGOS_EDAD = [(0, 6, 'Cachorro'), (6, 12, 'Joven'), (12, 24, 'Adulto joven'), (24, 84, 'Adulto'), (84, 999, 'Senior')]

# Ubicaciones comunes
UBICACIONES_COMUNES = ['Bogotá', 'Medellín', 'Cali', 'Barranquilla', 'Cartagena', ...]

# Razas comunes
RAZAS_PERROS = ['Labrador', 'Golden Retriever', 'Pastor Alemán', 'Bulldog', ...]
RAZAS_GATOS = ['Persa', 'Siamés', 'Maine Coon', 'British Shorthair', ...]
```

### 🔄 Relaciones entre Modelos

```
User (Django Auth)
├── mascotas_registradas (Mascota) → responsable
├── solicitudes_adopcion (SolicitudAdopcion) → usuario
├── filtros_busqueda (FiltroBusqueda) → usuario
└── historial_busquedas (HistorialBusqueda) → usuario

Mascota
├── solicitudes (SolicitudAdopcion) → mascota
└── Usado por FiltroBusqueda.aplicar_filtro()

FiltroBusqueda
└── historial_busquedas (HistorialBusqueda) → filtro_aplicado
```

## 📱 Apps del Proyecto

### 🐕 Registro de Mascotas
- Registro de mascotas
- Información detallada (edad, raza, tamaño, etc.)
- Galería de fotos
- Estado de adopción

### 🏠 Solicitud de Adopción
- Proceso de adopción
- Formularios de solicitud de adopción
- Seguimiento de adopciones
- Historial de adopciones

### 🔍 Sistema de Filtros
- **Filtros básicos**: Por especie (perro, gato, otro), sexo, edad y ubicación
- **Filtros avanzados**: Por raza específica, búsqueda de texto en nombre/descripción
- **Filtros guardados**: Los usuarios pueden guardar y reutilizar filtros personalizados
- **Historial de búsquedas**: Registro de todas las búsquedas realizadas
- **Filtros combinados**: Aplicar múltiples criterios simultáneamente
- **Filtros favoritos**: Marcar filtros como favoritos para acceso rápido

### 📝 Blog
- Artículos sobre cuidado de mascotas
- Noticias del refugio
- Consejos veterinarios
- Historias de adopción exitosas

## 💡 Ejemplos de Uso

### 🔍 Uso del Sistema de Filtros

```python
from registro_mascotas.models import Mascota
from filtros.models import FiltroBusqueda

# Filtrar por especie
perros = Mascota.filtrar_por_especie('perro')
gatos = Mascota.filtrar_por_especie('gato')

# Filtrar por edad
cachorros = Mascota.filtrar_por_edad(edad_max=12)  # Menos de 1 año
adultos = Mascota.filtrar_por_edad(edad_min=12, edad_max=84)  # 1-7 años

# Filtrar por ubicación
mascotas_bogota = Mascota.filtrar_por_ubicacion('Bogotá')

# Filtro combinado
perros_jovenes_bogota = Mascota.filtrar_combinado(
    tipo='perro',
    edad_max=24,
    ubicacion='Bogotá'
)

# Crear y usar filtro personalizado
filtro = FiltroBusqueda.objects.create(
    nombre_filtro="Perros jóvenes en Bogotá",
    tipo='perro',
    edad_max=24,
    ubicacion='Bogotá',
    es_favorito=True
)

# Aplicar filtro guardado
resultados = filtro.aplicar_filtro()
print(f"Encontrados {resultados.count()} perros jóvenes en Bogotá")

# Ver criterios activos
criterios = filtro.get_criterios_activos()
print("Criterios:", criterios)
```

### 🏠 Gestión de Solicitudes de Adopción

```python
from solicitud_adopcion.models import SolicitudAdopcion

# Crear solicitud de adopción
solicitud = SolicitudAdopcion.objects.create(
    usuario=usuario,
    mascota=mascota,
    mensaje="Me encantaría adoptar esta mascota porque..."
)

# Aprobar solicitud
solicitud.estado = 'aprobada'
solicitud.respuesta = "¡Felicidades! Tu solicitud ha sido aprobada."
solicitud.fecha_respuesta = timezone.now()
solicitud.save()

# Cambiar estado de la mascota
mascota.estado = 'adoptado'
mascota.save()
```

### 📊 Consultas Avanzadas

```python
# Mascotas más populares (más solicitudes)
from django.db.models import Count
mascotas_populares = Mascota.objects.annotate(
    num_solicitudes=Count('solicitudes')
).order_by('-num_solicitudes')[:10]

# Usuarios más activos en adopciones
usuarios_activos = User.objects.annotate(
    num_solicitudes=Count('solicitudes_adopcion')
).order_by('-num_solicitudes')[:10]

# Estadísticas por tipo de mascota
from django.db.models import Count
estadisticas = Mascota.objects.values('tipo').annotate(
    total=Count('id'),
    disponibles=Count('id', filter=models.Q(estado='disponible'))
)
```

## 🔧 Configuración

### Variables de Entorno

Para producción, configura las siguientes variables:

```python
# En settings.py
DEBUG = False
ALLOWED_HOSTS = ['tu-dominio.com']
SECRET_KEY = 'tu-clave-secreta-aqui'
```

### Base de Datos

El proyecto está configurado para usar SQLite por defecto. Para producción, puedes cambiar a PostgreSQL o MySQL:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'portal_mascotas',
        'USER': 'usuario',
        'PASSWORD': 'contraseña',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👥 Autores

- **Tornadusk** - *Desarrollo inicial* - [GitHub](https://github.com/Tornadusk)

## 📞 Contacto

Si tienes preguntas o sugerencias, no dudes en contactarnos:

- GitHub: [@Tornadusk](https://github.com/Tornadusk)
- Email: [tu-email@ejemplo.com]

## 🙏 Agradecimientos

- Django Software Foundation
- Comunidad de Python
- Todos los contribuidores del proyecto

## 📊 Modelo Entidad-Relación (M.E.R)

### 🏗️ Diagrama de Entidades

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     Usuario     │    │     Mascota     │    │ Solicitud_      │
│                 │    │                 │    │ Adopcion        │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ id_usuario (PK) │    │ id_mascota (PK) │    │ id_solicitud    │
│ username        │    │ nombre          │    │ (PK)            │
│ email           │    │ tipo            │    │ id_usuario (FK) │
│ password        │    │ raza            │    │ id_mascota (FK) │
│ fecha_creacion  │    │ edad            │    │ mensaje         │
│ fecha_actualiz. │    │ sexo            │    │ fecha_solicitud │
└─────────────────┘    │ descripcion     │    │ fecha_respuesta │
         │              │ ubicacion       │    │ estado          │
         │              │ foto            │    │ respuesta       │
         │              │ estado          │    └─────────────────┘
         │              │ id_responsable  │             │
         │              │ (FK)            │             │
         │              └─────────────────┘             │
         │                       │                      │
         │                       │                      │
         │              ┌─────────────────┐             │
         │              │ Filtro_Busqueda │             │
         │              │                 │             │
         │              ├─────────────────┤             │
         │              │ id_filtro (PK)  │             │
         │              │ id_usuario (FK) │             │
         │              │ tipo_mascota    │             │
         │              │ sexo            │             │
         │              │ edad_min        │             │
         │              │ edad_max        │             │
         │              │ ubicacion       │             │
         │              └─────────────────┘             │
         │                       │                      │
         │                       │                      │
         │              ┌─────────────────┐             │
         │              │ Historial_      │             │
         │              │ Busqueda        │             │
         │              │                 │             │
         │              ├─────────────────┤             │
         │              │ id_historial    │             │
         │              │ (PK)            │             │
         │              │ id_usuario (FK) │             │
         │              │ id_mascota (FK) │             │
         │              │ fecha_busqueda  │             │
         │              │ criterios_busq. │             │
         │              └─────────────────┘             │
         │                       │                      │
         └───────────────────────┼──────────────────────┘
                                 │
                                 │
                    ┌─────────────────┐
                    │     Blog        │
                    │   (Opcional)    │
                    │                 │
                    ├─────────────────┤
                    │ id_post (PK)    │
                    │ titulo          │
                    │ contenido       │
                    │ autor (FK)      │
                    │ fecha_public.   │
                    │ estado          │
                    └─────────────────┘
```

### 🔗 Relaciones Implementadas

| Entidad 1 | Relación | Entidad 2 | Descripción |
|-----------|----------|-----------|-------------|
| Usuario | 1:N | Mascota | Un usuario puede registrar múltiples mascotas |
| Usuario | 1:N | Solicitud_Adopcion | Un usuario puede hacer múltiples solicitudes |
| Mascota | 1:N | Solicitud_Adopcion | Una mascota puede tener múltiples solicitudes |
| Usuario | 1:N | Filtro_Busqueda | Un usuario puede crear múltiples filtros |
| Usuario | 1:N | Historial_Busqueda | Un usuario tiene múltiples búsquedas |
| Mascota | 1:N | Historial_Busqueda | Una mascota aparece en múltiples búsquedas |
| Usuario | 1:N | Blog (Post) | Un usuario puede escribir múltiples posts |

### 📋 Campos Clave por Entidad

#### 👤 Usuario
- **PK**: `id_usuario` (auto-incremento)
- **Únicos**: `username`, `email`
- **Obligatorios**: `username`, `email`, `password`
- **Auditoría**: `fecha_creacion`, `fecha_actualizacion`

#### 🐕 Mascota
- **PK**: `id_mascota` (auto-incremento)
- **FK**: `id_responsable` → Usuario
- **Obligatorios**: `nombre`, `tipo`, `responsable`
- **Opcionales**: `foto`, `descripcion`, `raza`

#### 📝 Solicitud_Adopcion
- **PK**: `id_solicitud` (auto-incremento)
- **FK**: `id_usuario` → Usuario, `id_mascota` → Mascota
- **Estados**: `pendiente`, `aprobada`, `rechazada`, `cancelada`
- **Validaciones**: No duplicar solicitudes del mismo usuario para la misma mascota

#### 🔍 Filtro_Busqueda
- **PK**: `id_filtro` (auto-incremento)
- **FK**: `id_usuario` → Usuario
- **Funcionalidad**: Guardar criterios de búsqueda personalizados

#### 📊 Historial_Busqueda
- **PK**: `id_historial` (auto-incremento)
- **FK**: `id_usuario` → Usuario, `id_mascota` → Mascota
- **Propósito**: Registrar todas las búsquedas realizadas

## 🏗️ Estructura Completa del Proyecto

```
PortalMascotas/
├── registro_mascotas/          # App para registro de mascotas
│   ├── models.py              # Modelo Mascota
│   ├── views.py               # Vistas para gestión de mascotas
│   ├── admin.py               # Configuración del admin
│   └── migrations/            # Migraciones de base de datos
├── solicitud_adopcion/        # App para solicitudes de adopción
│   ├── models.py              # Modelo SolicitudAdopcion
│   ├── views.py               # Vistas para solicitudes
│   ├── urls.py                # URLs de la app
│   ├── admin.py               # Configuración del admin
│   ├── templates/             # Templates HTML
│   │   └── solicitud_adopcion/
│   ├── static/                # Archivos estáticos (CSS, JS)
│   │   └── solicitud_adopcion/
│   └── migrations/            # Migraciones de base de datos
├── filtros/                   # App para filtros y búsquedas
│   ├── models.py              # Modelos FiltroBusqueda y HistorialBusqueda
│   ├── views.py               # Vistas para filtros
│   └── migrations/            # Migraciones de base de datos
├── login/                     # App para autenticación
│   ├── models.py              # Modelo Usuario personalizado
│   ├── views.py               # Vistas de login, registro, perfil
│   ├── urls.py                # URLs de autenticación
│   ├── admin.py               # Configuración del admin
│   ├── templates/             # Templates de login y registro
│   │   └── login/
│   └── migrations/            # Migraciones de base de datos
├── blog/                      # App para blog y artículos (deshabilitada)
│   ├── models.py              # Modelos Post, Category, Comment
│   ├── views.py               # Vistas del blog
│   ├── urls.py                # URLs del blog
│   ├── admin.py               # Configuración del admin
│   ├── templates/             # Templates del blog
│   │   └── blog/
│   └── migrations/            # Migraciones de base de datos
├── portal_mascotas/           # Configuración del proyecto principal
│   ├── settings.py            # Configuraciones del proyecto
│   ├── urls.py                # URLs principales
│   ├── wsgi.py                # Configuración WSGI
│   ├── asgi.py                # Configuración ASGI
│   ├── constantes.py          # Constantes centralizadas
│   ├── templates/             # Templates globales
│   │   └── portal_mascotas/
│   └── views.py               # Vistas principales (dashboard)
├── static/                    # Archivos estáticos globales
│   ├── css/                   # CSS globales
│   │   ├── main.css           # Estilos principales
│   │   └── auth.css           # Estilos de autenticación
│   └── js/                    # JavaScript global
│       ├── main.js            # JS principal
│       └── auth.js            # JS de autenticación
├── templates/                 # Templates globales (si se usa)
├── venv/                      # Entorno virtual (no incluir en Git)
├── manage.py                  # Script de administración de Django
├── requirements.txt           # Dependencias del proyecto
└── README.txt                 # Documentación del proyecto
```

---

⭐ ¡No olvides darle una estrella al proyecto si te gusta!
