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

# --- Filtros geográficos por región y ciudad/comuna ---
REGIONES_CIUDADES = {
    "Región de Arica y Parinacota": ["Arica", "Putre"],
    "Región de Tarapacá": ["Área Metropolitana Alto Hospicio–Iquique", "Pozo Almonte"],
    "Región de Antofagasta": ["Antofagasta", "Mejillones", "Taltal", "Calama", "San Pedro de Atacama", "Tocopilla"],
    "Región de Atacama": ["Copiapó", "Caldera", "Tierra Amarilla", "Chañaral", "Diego de Almagro", "El Salvador", "Vallenar", "Huasco"],
    "Región de Coquimbo": ["Conurbación La Serena–Coquimbo (La Serena y Coquimbo)", "Tongoy", "Andacollo", "Vicuña", "Illapel", "Los Vilos", "Canela", "Salamanca", "Ovalle", "Combarbalá", "Monte Patria", "El Palqui", "Punitaqui"],
    "Región de Valparaíso": [
        "Gran Valparaíso (Valparaíso, Viña del Mar, Concón, Quilpué y Villa Alemana)", "Casablanca", "Puchuncaví", "Las Ventanas", "Quintero",
        "Hanga Roa", "Juan Fernández", "Los Andes (Los Andes y Calle Larga)", "Rinconada", "San Esteban", "La Ligua", "Cabildo",
        "Gran Quillota (Quillota, La Calera, Hijuelas y La Cruz)", "Nogales", "El Melón",
        "Gran San Antonio (San Antonio, Cartagena, Las Cruces y Santo Domingo)", "Algarrobo–El Quisco–El Tabo", "Mirasol–El Yeco",
        "San Felipe (San Felipe, Villa Los Almendros, Santa María)", "Catemu", "Llay-Llay", "Putaendo", "Limache–Olmué"
    ],
    "Región del Libertador B. O’Higgins": [
        "Gran Rancagua (Rancagua, Machalí, Gultro, Los Lirios)", "Codegua", "Coltauco", "Doñihue", "Lo Miranda", "Graneros",
        "Las Cabras (Las Cabras, Punta Diamante)", "San Francisco de Mostazal", "La Punta", "Peumo", "Pichidegua",
        "Quinta de Tilcoco", "Rengo", "Requínoa", "San Vicente de Tagua Tagua", "Pichilemu", "San Fernando",
        "Chépica", "Chimbarongo", "Nancagua", "Peralillo"
    ],
    "Región del Maule": [
        "Gran Talca (Talca y Maule Norte)", "Maule", "San Clemente", "Constitución", "Cauquenes",
        "Curicó", "Molina", "Hualañé", "Rauco", "Romeral", "Teno",
        "Linares", "Colbún", "Longaví", "Parral", "Retiro", "San Javier", "Villa Alegre"
    ],
    "Región de Ñuble": ["Chillán (Chillán y Chillán Viejo)", "Coelemu", "Quirihue", "Bulnes", "Quillón", "Yungay", "Coihueco", "San Carlos"],
    "Región del Biobío": [
        "Gran Concepción (Concepción, Talcahuano, Chiguayante, Hualpén, Penco, San Pedro de la Paz)", "Coronel", "Hualqui", "Lota", "Santa Juana",
        "Tomé", "Lebu", "Arauco", "Laraquete", "Cañete", "Curanilahue", "Los Álamos", "Contulmo", "Los Ángeles", "Cabrero",
        "Conurbación La Laja–San Rosendo", "Monte Águila", "Mulchén", "Nacimiento", "Santa Bárbara", "Huépil", "Yumbel", "Florida"
    ],
    "Región de La Araucanía": [
        "Gran Temuco (Temuco y Padre Las Casas)", "Angol", "Padre Las Casas", "Villarrica", "Victoria", "Lautaro", "Temuco",
        "Nueva Imperial", "Pucón", "Pitrufquén", "Collipulli", "Loncoche", "Traiguén", "Curacautín", "Carahue", "Gorbea",
        "Purén", "Cunco", "Renaico", "Vilcún", "Cajón", "Freire"
    ],
    "Región de Los Ríos": ["Corral", "Lanco", "Los Lagos", "San José de la Mariquina", "Paillaco", "Panguipulli", "La Unión", "Futrono", "Río Bueno", "Valdivia", "Máfil"],
    "Región de Los Lagos": ["Gran Puerto Montt (Puerto Montt, Alerce, Puerto Varas)", "Calbuco", "Fresia", "Frutillar", "Los Muermos", "Llanquihue", "Castro", "Ancud", "Chonchi", "Dalcahue", "Quellón", "Osorno", "Purranque", "Río Negro", "Chaitén"],
    "Región de Aysén del Gral. C. Ibáñez del Campo": ["Coyhaique", "Puerto Aysén", "Cochrane", "Chile Chico"],
    "Región de Magallanes y de la Antártica Chilena": ["Punta Arenas", "Puerto Williams", "Porvenir", "Puerto Natales"],
    "Región Metropolitana de Santiago": [
        "Santiago","Cerrillos","Cerro Navia","Conchalí","El Bosque","Estación Central","Huechuraba","Independencia","La Cisterna",
        "La Florida","La Granja","La Pintana","La Reina","Las Condes","Lo Barnechea","Lo Espejo","Lo Prado","Macul","Maipú","Ñuñoa",
        "Pedro Aguirre Cerda","Peñalolén","Providencia","Pudahuel","Quilicura","Quinta Normal","Recoleta","Renca","San Joaquín",
        "San Miguel","San Ramón","Vitacura","Puente Alto","Pirque","San José de Maipo","Colina","Lampa","Tiltil","San Bernardo",
        "Buin","Calera de Tango","Paine","María Pinto","Talagante","El Monte","Isla de Maipo","Padre Hurtado","Peñaflor"
    ],
}

