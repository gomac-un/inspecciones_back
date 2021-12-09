# Generated by Django 3.2.8 on 2021-12-06 17:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Activo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identificador', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='Bloque',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('n_orden', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CriticidadNumerica',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('valor_minimo', models.FloatField()),
                ('valor_maximo', models.FloatField()),
                ('criticidad', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Cuestionario',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('tipo_de_inspeccion', models.CharField(max_length=500)),
                ('version', models.IntegerField()),
                ('periodicidad_dias', models.IntegerField()),
                ('momento_subida', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='EtiquetaDeActivo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clave', models.CharField(max_length=200)),
                ('valor', models.CharField(max_length=200)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EtiquetaDePregunta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clave', models.CharField(max_length=200)),
                ('valor', models.CharField(max_length=200)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Inspeccion',
            fields=[
                ('id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('momento_inicio', models.DateTimeField()),
                ('momento_finalizacion', models.DateTimeField(null=True)),
                ('momento_subida', models.DateTimeField(auto_now_add=True)),
                ('estado', models.CharField(choices=[('borrador', 'Borrador'), ('en_reparacion', 'En Reparacion'), ('finalizada', 'Finalizada')], max_length=50)),
                ('criticidad_calculada', models.IntegerField()),
                ('criticidad_calculada_con_reparaciones', models.IntegerField()),
                ('activo', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='inspecciones', to='inspecciones.activo')),
                ('cuestionario', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='inspecciones', to='inspecciones.cuestionario')),
            ],
        ),
        migrations.CreateModel(
            name='OpcionDeRespuesta',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('titulo', models.CharField(max_length=500)),
                ('descripcion', models.CharField(blank=True, max_length=1500)),
                ('criticidad', models.IntegerField()),
                ('requiere_criticidad_del_inspector', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Organizacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=120, unique=True)),
                ('logo', models.ImageField(default='blank.jpg', upload_to='logos_organizaciones')),
                ('link', models.URLField(blank=True)),
                ('acerca', models.TextField(blank=True)),
                ('caracteristicas', multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('reparaciones', 'Reparaciones'), ('planeacion', 'Planeacion')], max_length=23)),
            ],
        ),
        migrations.CreateModel(
            name='Pregunta',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('titulo', models.CharField(max_length=500)),
                ('descripcion', models.CharField(blank=True, max_length=1500)),
                ('criticidad', models.IntegerField()),
                ('tipo_de_pregunta', models.CharField(choices=[('cuadricula', 'Cuadricula'), ('parte_de_cuadricula', 'Parte De Cuadricula'), ('seleccion_unica', 'Seleccion Unica'), ('seleccion_multiple', 'Seleccion Multiple'), ('numerica', 'Numerica')], max_length=50)),
                ('tipo_de_cuadricula', models.CharField(choices=[('seleccion_unica', 'Seleccion Unica'), ('seleccion_multiple', 'Seleccion Multiple')], max_length=50, null=True)),
                ('unidades', models.CharField(blank=True, max_length=20, null=True)),
                ('bloque', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pregunta', to='inspecciones.bloque')),
                ('cuadricula', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='preguntas', to='inspecciones.pregunta')),
                ('etiquetas', models.ManyToManyField(related_name='preguntas', to='inspecciones.EtiquetaDePregunta')),
            ],
        ),
        migrations.CreateModel(
            name='Titulo',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('titulo', models.CharField(max_length=500)),
                ('descripcion', models.CharField(blank=True, max_length=1500)),
                ('bloque', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='titulo', to='inspecciones.bloque')),
            ],
        ),
        migrations.CreateModel(
            name='Respuesta',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('observacion', models.CharField(blank=True, max_length=1500)),
                ('reparado', models.BooleanField()),
                ('observacion_reparacion', models.CharField(blank=True, max_length=1500)),
                ('momento_respuesta', models.DateTimeField(blank=True, null=True)),
                ('tipo_de_respuesta', models.CharField(choices=[('cuadricula', 'Cuadricula'), ('seleccion_unica', 'Seleccion Unica'), ('seleccion_multiple', 'Seleccion Multiple'), ('parte_de_seleccion_multiple', 'Parte De Seleccion Multiple'), ('numerica', 'Numerica')], max_length=50)),
                ('criticidad_del_inspector', models.IntegerField(blank=True, null=True)),
                ('criticidad_calculada', models.IntegerField()),
                ('criticidad_calculada_con_reparaciones', models.IntegerField()),
                ('opcion_respondida_esta_seleccionada', models.BooleanField(null=True)),
                ('valor_numerico', models.FloatField(null=True)),
                ('inspeccion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='respuestas', to='inspecciones.inspeccion')),
                ('opcion_respondida', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='respuestas_pregunta_de_seleccion_multiple', to='inspecciones.opcionderespuesta')),
                ('opcion_seleccionada', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='respuestas_pregunta_de_seleccion_unica', to='inspecciones.opcionderespuesta')),
                ('pregunta', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='respuestas', to='inspecciones.pregunta')),
                ('respuesta_cuadricula', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subrespuestas_cuadricula', to='inspecciones.respuesta')),
                ('respuesta_multiple', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subrespuestas_multiple', to='inspecciones.respuesta')),
            ],
        ),
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('celular', models.CharField(blank=True, max_length=13)),
                ('foto', models.ImageField(default='blank.jpg', upload_to='fotos_perfiles')),
                ('rol', models.CharField(choices=[('inspector', 'Inspector'), ('administrador', 'Administrador')], max_length=20)),
                ('organizacion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='usuarios', to='inspecciones.organizacion')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='opcionderespuesta',
            name='pregunta',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='opciones_de_respuesta', to='inspecciones.pregunta'),
        ),
        migrations.AddField(
            model_name='inspeccion',
            name='inspector',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='inspecciones_llenadas', to='inspecciones.perfil'),
        ),
        migrations.CreateModel(
            name='FotoRespuesta',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('foto', models.ImageField(upload_to='fotos_inspecciones')),
                ('tipo', models.CharField(choices=[('base', 'Base'), ('reparacion', 'Reparacion')], max_length=50)),
                ('respuesta', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fotos', to='inspecciones.respuesta')),
            ],
        ),
        migrations.CreateModel(
            name='FotoCuestionario',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('foto', models.ImageField(upload_to='fotos_cuestionarios')),
                ('object_id', models.UUIDField(null=True)),
                ('content_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
        ),
        migrations.CreateModel(
            name='EtiquetaJerarquicaDePregunta',
            fields=[
                ('nombre', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('json', models.JSONField()),
                ('organizacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='etiquetas_de_pregunta', to='inspecciones.organizacion')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EtiquetaJerarquicaDeActivo',
            fields=[
                ('nombre', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('json', models.JSONField()),
                ('organizacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='etiquetas_de_activo', to='inspecciones.organizacion')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddConstraint(
            model_name='etiquetadepregunta',
            constraint=models.UniqueConstraint(fields=('clave', 'valor'), name='inspecciones_etiquetadepregunta_natural_key'),
        ),
        migrations.AddConstraint(
            model_name='etiquetadeactivo',
            constraint=models.UniqueConstraint(fields=('clave', 'valor'), name='inspecciones_etiquetadeactivo_natural_key'),
        ),
        migrations.AddField(
            model_name='cuestionario',
            name='creador',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cuestionarios_creados', to='inspecciones.perfil'),
        ),
        migrations.AddField(
            model_name='cuestionario',
            name='etiquetas_aplicables',
            field=models.ManyToManyField(related_name='cuestionarios', to='inspecciones.EtiquetaDeActivo'),
        ),
        migrations.AddField(
            model_name='cuestionario',
            name='organizacion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cuestionarios', to='inspecciones.organizacion'),
        ),
        migrations.AddField(
            model_name='criticidadnumerica',
            name='pregunta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='criticidades_numericas', to='inspecciones.pregunta'),
        ),
        migrations.AddField(
            model_name='bloque',
            name='cuestionario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bloques', to='inspecciones.cuestionario'),
        ),
        migrations.AddField(
            model_name='activo',
            name='etiquetas',
            field=models.ManyToManyField(related_name='activos', to='inspecciones.EtiquetaDeActivo'),
        ),
        migrations.AddField(
            model_name='activo',
            name='organizacion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activos', to='inspecciones.organizacion'),
        ),
        migrations.AddConstraint(
            model_name='respuesta',
            constraint=models.CheckConstraint(check=models.Q(models.Q(('tipo_de_respuesta', 'seleccion_unica'), ('opcion_seleccionada__isnull', False)), models.Q(models.Q(('tipo_de_respuesta', 'seleccion_unica'), _negated=True), models.Q(('opcion_seleccionada__isnull', False), _negated=True)), _connector='OR'), name='inspecciones_respuesta_unica_respuesta'),
        ),
        migrations.AddConstraint(
            model_name='pregunta',
            constraint=models.CheckConstraint(check=models.Q(models.Q(('bloque__isnull', False), models.Q(('cuadricula__isnull', False), _negated=True)), models.Q(models.Q(('bloque__isnull', False), _negated=True), ('cuadricula__isnull', False)), _connector='OR'), name='inspecciones_pregunta_padre'),
        ),
        migrations.AddConstraint(
            model_name='pregunta',
            constraint=models.CheckConstraint(check=models.Q(models.Q(('tipo_de_pregunta', 'cuadricula'), ('tipo_de_cuadricula__isnull', False)), models.Q(models.Q(('tipo_de_pregunta', 'cuadricula'), _negated=True), models.Q(('tipo_de_cuadricula__isnull', False), _negated=True)), _connector='OR'), name='inspecciones_pregunta_cuadricula'),
        ),
        migrations.AddConstraint(
            model_name='pregunta',
            constraint=models.CheckConstraint(check=models.Q(models.Q(('tipo_de_pregunta', 'parte_de_cuadricula'), ('cuadricula__isnull', False)), models.Q(models.Q(('tipo_de_pregunta', 'parte_de_cuadricula'), _negated=True), models.Q(('cuadricula__isnull', False), _negated=True)), _connector='OR'), name='inspecciones_pregunta_parte_de_cuadricula'),
        ),
        migrations.AddConstraint(
            model_name='cuestionario',
            constraint=models.UniqueConstraint(fields=('organizacion', 'tipo_de_inspeccion', 'version'), name='version de cuestionario'),
        ),
        migrations.AddConstraint(
            model_name='activo',
            constraint=models.UniqueConstraint(fields=('id', 'organizacion'), name='inspecciones_activo_natural_key'),
        ),
    ]
