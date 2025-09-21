# registro_mascotas/forms.py
from django import forms
from portal_mascotas.constantes import TIPOS_MASCOTA, SEXOS

# Clases CSS para que el formulario se vea uniforme (coinciden con tu home.html)
BASE_INPUT = {"class": "ap-input"}
BASE_SELECT = {"class": "ap-select"}
BASE_TEXTAREA = {"class": "ap-textarea", "rows": 4}
BASE_FILE = {"class": "ap-file"}

class PublicarMascotaForm(forms.Form):
    """
    Formulario para que el usuario proponga publicar una mascota.
    Replica los campos que usa el admin al crear Mascota.
    """
    nombre = forms.CharField(
        max_length=100, required=True, label='Nombre',
        widget=forms.TextInput(attrs=BASE_INPUT)
    )
    tipo = forms.ChoiceField(
        choices=TIPOS_MASCOTA, required=True, label='Tipo',
        widget=forms.Select(attrs=BASE_SELECT)
    )
    raza = forms.CharField(
        max_length=100, required=True, label='Raza',
        widget=forms.TextInput(attrs=BASE_INPUT)
    )
    edad = forms.IntegerField(
        min_value=0, required=True, label='Edad (meses)',
        widget=forms.NumberInput(attrs=BASE_INPUT)
    )
    sexo = forms.ChoiceField(
        choices=SEXOS, required=True, label='Sexo',
        widget=forms.Select(attrs=BASE_SELECT)
    )
    descripcion = forms.CharField(
        required=True, label='Descripción',
        widget=forms.Textarea(attrs=BASE_TEXTAREA)
    )
    ubicacion = forms.CharField(
        max_length=200, required=True, label='Ubicación',
        widget=forms.TextInput(attrs=BASE_INPUT)
    )
    # 🔒 Foto OBLIGATORIA
    # 🚫 Corregido: NO usar BASE_FILE | {"accept": "image/*"} (rompe en Python 3.8)
    # ✅ Usamos dict unpacking compatible con 3.8+
    foto = forms.ImageField(
        required=True, label='Foto',
        widget=forms.ClearableFileInput(attrs={**BASE_FILE, "accept": "image/*"})
    )

