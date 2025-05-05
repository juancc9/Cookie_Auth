from django.db import models

class Roles(models.Model):
    OPCIONES = [
        ('aprendiz', 'Aprendiz'),
        ('pasante', 'Pasante'),
        ('instructor', 'Instructor'),
        ('administrador', 'Administrador')
    ]
    
    nombre = models.CharField(max_length=20, choices=OPCIONES, unique=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.get_nombre_display()