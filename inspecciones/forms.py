from django import forms
from django_registration.forms import RegistrationForm

from inspecciones.models import Perfil


class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['celular', 'foto']


class UserForm(RegistrationForm):
    nombre = forms.CharField(label="Nombre")
    apellido = forms.CharField(label="Apellido")
