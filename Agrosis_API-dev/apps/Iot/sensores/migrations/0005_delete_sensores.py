# Generated by Django 5.1 on 2025-04-18 15:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datos_meteorologicos', '0006_alter_datos_metereologicos_fk_sensor'),
        ('sensores', '0004_sensor_remove_sensores_tipo_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Sensores',
        ),
    ]
