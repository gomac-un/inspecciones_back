# Generated by Django 4.0.3 on 2022-04-07 02:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inspecciones', '0009_alter_fotorespuesta_respuesta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fotorespuesta',
            name='respuesta',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fotos', to='inspecciones.respuesta'),
        ),
    ]
