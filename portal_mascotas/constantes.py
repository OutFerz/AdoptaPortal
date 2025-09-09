# Constantes compartidas para la aplicación de mascotas
# Este archivo centraliza las opciones que se usan en múltiples modelos

# Opciones para tipos de mascotas
TIPOS_MASCOTA = [
    ('perro', 'Perro'),
    ('gato', 'Gato'),
    ('otro', 'Otro'),
]

# Opciones para sexo de mascotas
SEXOS = [
    ('macho', 'Macho'),
    ('hembra', 'Hembra'),
]

# Opciones para estados de mascotas
ESTADOS_MASCOTA = [
    ('disponible', 'Disponible'),
    ('adoptado', 'Adoptado'),
    ('reservado', 'Reservado'),
]

# Opciones para estados de solicitudes de adopción
ESTADOS_SOLICITUD = [
    ('pendiente', 'Pendiente'),
    ('aprobada', 'Aprobada'),
    ('rechazada', 'Rechazada'),
    ('cancelada', 'Cancelada'),
]

# Rangos de edad comunes (en meses)
RANGOS_EDAD = [
    (0, 6, 'Cachorro (0-6 meses)'),
    (6, 12, 'Joven (6-12 meses)'),
    (12, 24, 'Adulto joven (1-2 años)'),
    (24, 84, 'Adulto (2-7 años)'),
    (84, 999, 'Senior (7+ años)'),
]

# Ubicaciones comunes (puedes expandir según tu región)
UBICACIONES_COMUNES = [
    'Bogotá',
    'Medellín',
    'Cali',
    'Barranquilla',
    'Cartagena',
    'Bucaramanga',
    'Pereira',
    'Santa Marta',
    'Ibagué',
    'Pasto',
]

# Razas comunes de perros
RAZAS_PERROS = [
    'Labrador',
    'Golden Retriever',
    'Pastor Alemán',
    'Bulldog',
    'Beagle',
    'Poodle',
    'Chihuahua',
    'Rottweiler',
    'Yorkshire',
    'Mestizo',
]

# Razas comunes de gatos
RAZAS_GATOS = [
    'Persa',
    'Siamés',
    'Maine Coon',
    'British Shorthair',
    'Ragdoll',
    'Bengala',
    'Abisinio',
    'Sphynx',
    'Mestizo',
]
