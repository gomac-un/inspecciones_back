from django.contrib import admin

# Register your models here.
from inspecciones.models import Organizacion, Perfil, Activo, Inspeccion, Respuesta, FotoRespuesta

admin.site.register(Organizacion)
admin.site.register(Perfil)
admin.site.register(Activo)
admin.site.register(Inspeccion)
admin.site.register(Respuesta)
admin.site.register(FotoRespuesta)