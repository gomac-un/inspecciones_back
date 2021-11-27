```
python manage.py makemigrations
python manage.py migrate

python manage.py loaddata organizacion_usuarios_y_perfiles
python manage.py loaddata activo_cuestionario_inspeccion
python manage.py dumpdata > dump.json

Get-Content inspecciones\pruebas_manuales\crear_primer_admin.py | python manage.py shell
python manage.py runserver
```