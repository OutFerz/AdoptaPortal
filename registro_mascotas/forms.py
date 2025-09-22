# registro_mascotas/forms.py
from django import forms
from django.core.validators import RegexValidator
from portal_mascotas.constantes import TIPOS_MASCOTA, SEXOS

# Clases CSS para que el formulario se vea uniforme (coinciden con tu home.html)
BASE_INPUT = {"class": "ap-input"}
BASE_SELECT = {"class": "ap-select"}
BASE_TEXTAREA = {"class": "ap-textarea", "rows": 4}
BASE_FILE = {"class": "ap-file"}

telefono_validator = RegexValidator(
    regex=r'^[0-9+\-\s()]{7,20}$',
    message='Ingresa un teléfono válido (solo números, +, -, espacios, paréntesis).'
)

class PublicarMascotaForm(forms.Form):
    """
    Formulario para que el usuario proponga publicar una mascota.
    Replica los campos del admin + datos de contacto del solicitante.
    """
    # ----- Mascota -----
    nombre = forms.CharField(max_length=100, required=True, label='Nombre',
                             widget=forms.TextInput(attrs={**BASE_INPUT, "placeholder": "Ej: Toby"}))
    tipo = forms.ChoiceField(choices=TIPOS_MASCOTA, required=True, label='Tipo',
                             widget=forms.Select(attrs=BASE_SELECT))
    raza = forms.CharField(max_length=100, required=True, label='Raza',
                           widget=forms.TextInput(attrs={**BASE_INPUT, "placeholder": "Ej: Mestizo"}))
    edad = forms.IntegerField(min_value=0, required=True, label='Edad (meses)',
                              widget=forms.NumberInput(attrs=BASE_INPUT))
    sexo = forms.ChoiceField(choices=SEXOS, required=True, label='Sexo',
                             widget=forms.Select(attrs=BASE_SELECT))
    descripcion = forms.CharField(required=True, label='Descripción',
                                  widget=forms.Textarea(attrs={**BASE_TEXTAREA, "placeholder": "Carácter, salud, vacunas…"}))
    ubicacion = forms.CharField(max_length=200, required=True, label='Ubicación',
                                widget=forms.TextInput(attrs={**BASE_INPUT, "placeholder": "Ciudad/Región"}))
    # Foto OBLIGATORIA
    foto = forms.ImageField(required=True, label='Foto',
                            widget=forms.ClearableFileInput(attrs={**BASE_FILE, "accept": "image/*"}))

    # ----- Contacto de la persona -----
    contacto_nombre = forms.CharField(max_length=100, required=True, label='Nombre de contacto',
                                      widget=forms.TextInput(attrs={**BASE_INPUT, "placeholder": "Nombre y apellido"}))
    contacto_email = forms.EmailField(required=True, label='Correo',
                                      widget=forms.EmailInput(attrs={**BASE_INPUT, "placeholder": "nombre@correo.com"}))
    contacto_direccion = forms.CharField(max_length=200, required=True, label='Dirección',
                                         widget=forms.TextInput(attrs={**BASE_INPUT, "placeholder": "Calle, número, ciudad"}))
    contacto_telefono = forms.CharField(max_length=30, required=True, label='Teléfono',
                                        validators=[telefono_validator],
                                        widget=forms.TextInput(attrs={**BASE_INPUT, "placeholder": "+56 9 1234 5678"}))

    # Seguridad extra
    acepta_declaracion = forms.BooleanField(
        required=True,
        label='Declaro que la información proporcionada es verídica y que soy responsable de esta publicación.'
    )

