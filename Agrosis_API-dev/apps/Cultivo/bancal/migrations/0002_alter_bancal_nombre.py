# Generated by Django 5.1 on 2025-02-20 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bancal', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bancal',
            name='nombre',
            field=models.CharField(max_length=15, unique=True),
        ),
    ]
