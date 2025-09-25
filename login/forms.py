# login/forms.py
from django import forms

class LoginForm(forms.Form):
    usuario_o_email = forms.CharField(
        label="Usuario o Correo",
        max_length=254,
        widget=forms.TextInput(attrs={
            "placeholder": "tu_usuario o tu@correo.com",
            "autocomplete": "username",
        }),
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )
