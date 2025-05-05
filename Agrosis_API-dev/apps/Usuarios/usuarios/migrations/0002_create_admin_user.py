from django.db import migrations
from django.contrib.auth.hashers import make_password

def create_admin_user(apps, schema_editor):
    Usuarios = apps.get_model('usuarios', 'Usuarios')
    Roles = apps.get_model('roles', 'Roles')
    admin_role = Roles.objects.get(id=4)

    # Obtener el rol de administrador
    admin_role = Roles.objects.filter(nombre='Administrador').first()
    if not admin_role:
        return  # Si no existe el rol, salir
    
    # Crear el usuario administrador si no existe
    Usuarios.objects.get_or_create(
        email='admin01@gmail.com',
        defaults={
            'username': '@admin#',
            'nombre': 'Administer',
            'apellido': 'Userauth',
            'password': make_password('admin'),  
            'rol': admin_role,
            'is_staff': True,
            'is_superuser': True,
        }
    )

class Migration(migrations.Migration):
    dependencies = [
        ('usuarios', '0001_initial'),
        ('roles', '0002_auto_20250312_1419'),  # Ajusta esto según el nombre real de la migración de roles
    ]

    operations = [
        migrations.RunPython(create_admin_user),
    ]
