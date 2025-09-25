# registro_mascotas/forms.py
from django import forms
from django.core.validators import RegexValidator
from .models import SolicitudPublicacion

# Clases CSS (coinciden con tu home.html)
BASE_INPUT = {"class": "ap-input"}
BASE_SELECT = {"class": "ap-select"}
BASE_TEXTAREA = {"class": "ap-textarea", "rows": 4}
BASE_FILE = {"class": "ap-file"}

telefono_validator = RegexValidator(
    regex=r'^[0-9+\-\s()]{7,20}$',
    message='Ingresa un teléfono válido (solo números, +, -, espacios, paréntesis).'
)

class SolicitudPublicacionForm(forms.ModelForm):
    """
    ModelForm para crear SolicitudPublicacion manteniendo el estilo y
    la validación que usabas antes.
    """
    # Seguridad
    acepta_declaracion = forms.BooleanField(
        required=True,
        label='Declaro que la información proporcionada es verídica y que soy responsable de esta publicación.'
    )

    # Campos de contacto (opcionales aquí; si quieres mostrarlos en la UI,
    # inclúyelos en tu template)
    contacto_nombre = forms.CharField(
        max_length=100, required=False, label='Nombre de contacto',
        widget=forms.TextInput(attrs={**BASE_INPUT, "placeholder": "Nombre y apellido"})
    )
    contacto_email = forms.EmailField(
        required=False, label='Correo',
        widget=forms.EmailInput(attrs={**BASE_INPUT, "placeholder": "nombre@correo.com"})
    )
    contacto_direccion = forms.CharField(
        max_length=200, required=False, label='Dirección',
        widget=forms.TextInput(attrs={**BASE_INPUT, "placeholder": "Calle, número, ciudad"})
    )
    contacto_telefono = forms.CharField(
        max_length=30, required=False, label='Teléfono',
        validators=[telefono_validator],
        widget=forms.TextInput(attrs={**BASE_INPUT, "placeholder": "+56 9 1234 5678"})
    )

    class Meta:
        model = SolicitudPublicacion
        fields = (
            # Datos de la mascota
            "nombre", "tipo", "sexo", "raza", "edad",
            "ubicacion", "descripcion", "foto",
            # Contacto (opcionales en el form)
            "contacto_nombre", "contacto_email", "contacto_direccion", "contacto_telefono",
            # Seguridad
            "acepta_declaracion",
        )
        widgets = {
            "nombre":      forms.TextInput(attrs={**BASE_INPUT, "placeholder": "Ej: Toby"}),
            "tipo":        forms.Select(attrs=BASE_SELECT),
            "sexo":        forms.Select(attrs=BASE_SELECT),
            "raza":        forms.TextInput(attrs={**BASE_INPUT, "placeholder": "Ej: Mestizo"}),
            "edad":        forms.NumberInput(attrs={**BASE_INPUT, "min": 0}),
            "ubicacion":   forms.TextInput(attrs={**BASE_INPUT, "placeholder": "Ciudad/Región"}),
            "descripcion": forms.Textarea(attrs={**BASE_TEXTAREA, "placeholder": "Carácter, salud, vacunas…"}),
            "foto":        forms.ClearableFileInput(attrs={**BASE_FILE, "accept": "image/*"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Asegurar que la foto sea obligatoria (aunque el modelo permita blank=True)
        self.fields["foto"].required = True

    def clean(self):
        cleaned = super().clean()
        # Si quieres forzar contacto cuando el usuario no tiene email en el perfil,
        # podrías descomentar lo siguiente:
        # if not cleaned.get("contacto_email"):
        #     raise forms.ValidationError("Debes indicar un correo de contacto.")
        return cleaned