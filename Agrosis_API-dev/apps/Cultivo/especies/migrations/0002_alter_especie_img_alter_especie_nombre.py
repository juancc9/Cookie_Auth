# Generated by Django 5.1 on 2025-02-20 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('especies', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='especie',
            name='img',
            field=models.ImageField(null=True, upload_to='especies_images/'),
        ),
        migrations.AlterField(
            model_name='especie',
            name='nombre',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]
