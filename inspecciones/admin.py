from django.contrib import admin

# Register your models here.
from inspecciones.models import Organizacion, Perfil

admin.site.register(Organizacion)
admin.site.register(Perfil)