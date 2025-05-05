from django.db import migrations

def create_initial_roles(apps, schema_editor):
    Roles = apps.get_model('roles', 'Roles')

    # Crear roles
    roles = ['Invitado', 'Pasante', 'Instructor', 'Administrador']
    for rol in roles:
        Roles.objects.get_or_create(nombre=rol)

class Migration(migrations.Migration):
    dependencies = [
        ('roles', '0001_initial'), 
    ]

    operations = [
        migrations.RunPython(create_initial_roles),
    ]
