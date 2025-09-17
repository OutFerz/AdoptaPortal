# portal_mascotas/constantes.py
# -*- coding: utf-8 -*-

TIPOS_MASCOTA = [
    ('perro', 'Perro'),
    ('gato', 'Gato'),
    ('conejo', 'Conejo'),
    ('ave', 'Ave'),
    ('hamster', 'Hámster'),
    ('Pez', 'Pez'),
    ('Tortuga', 'Tortuga'),	
    ('otro', 'Otro'),
]

SEXOS = [
    ('macho', 'Macho'),
    ('hembra', 'Hembra'),
]

ESTADOS_MASCOTA = [
    ('disponible', 'Disponible'),
    ('adoptado', 'Adoptado'),
    ('reservado', 'Reservado'),
]

ESTADOS_SOLICITUD = [
    ('pendiente', 'Pendiente'),
    ('aprobada', 'Aprobada'),
    ('rechazada', 'Rechazada'),
    ('cancelada', 'Cancelada'),
]

RANGOS_EDAD = [
    (0, 6, 'Cachorro (0-6 meses)'),
    (6, 12, 'Joven (6-12 meses)'),
    (12, 24, 'Adulto joven (1-2 años)'),
    (24, 84, 'Adulto (2-7 años)'),
    (84, 999, 'Senior (7+ años)'),
]

UBICACIONES_COMUNES = [
    'Bogotá','Medellín','Cali','Barranquilla','Cartagena',
    'Bucaramanga','Pereira','Santa Marta','Ibagué','Pasto',
]

RAZAS_PERROS = [
    'Labrador','Golden Retriever','Pastor Alemán','Bulldog','Beagle',
    'Poodle','Chihuahua','Rottweiler','Yorkshire','Mestizo',
]

RAZAS_GATOS = [
    'Persa','Siamés','Maine Coon','British Shorthair','Ragdoll',
    'Bengala','Abisinio','Sphynx','Mestizo',
]
