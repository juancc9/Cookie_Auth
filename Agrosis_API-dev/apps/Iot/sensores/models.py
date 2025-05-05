from django.db import models

class TipoSensor(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    unidad_medida = models.CharField(max_length=10)
    medida_minima = models.DecimalField(max_digits=10, decimal_places=2)
    medida_maxima = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

class Sensor(models.Model):
    nombre = models.CharField(max_length=100)
    tipo_sensor = models.CharField(max_length=50)
    unidad_medida = models.CharField(max_length=10)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre