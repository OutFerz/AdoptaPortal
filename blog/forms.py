from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["name", "email", "body"]
        labels = {
            "name": "Nombre",
            "email": "Email",
            "body": "Comentario",
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "input", "placeholder": "Tu nombre"}),
            "email": forms.EmailInput(attrs={"class": "input", "placeholder": "tucorreo@ejemplo.com"}),
            "body": forms.Textarea(attrs={"class": "input", "rows": 4, "placeholder": "Escribe tu comentario…"}),
        }