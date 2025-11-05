from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from core.models import User
from django.utils.translation import gettext_lazy as _

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "role"]
        labels = {
            "username": _("Nombre de usuario"),
            "email": _("Correo electrónico"),
            "password1": _("Contraseña"),
            "password2": _("Confirmar contraseña"),
            "role": _("Rol"),
        }

class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Usuario'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Contraseña'
        })
        self.fields['username'].label = _("Nombre de usuario")
        self.fields['password'].label = _("Contraseña")