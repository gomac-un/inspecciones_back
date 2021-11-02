from django.contrib.auth import get_user_model

from inspecciones.models import Organizacion, Perfil

user = get_user_model().objects.create_user(username='gato', password='gato', first_name="administrador")
organizacion = Organizacion.objects.create(nombre="gomac")
perfil = Perfil.objects.create(user=user, celular="123", organizacion=organizacion,
                               rol=Perfil.Roles.administrador)

# python manage.py makemigrations
# python manage.py migrate
# Get-Content inspecciones\crear_primer_admin.py | python manage.py shell
# python manage.py runserver