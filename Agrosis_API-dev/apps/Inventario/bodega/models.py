from django.db import models

class Bodega(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=50)
    activo = models.BooleanField(default=True)
    capacidad = models.PositiveIntegerField(default=100)  
    ubicacion = models.CharField(max_length=255, blank=True, null=True) 

    def __str__(self):
        return self.nombre
