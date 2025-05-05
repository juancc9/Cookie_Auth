from django.db import models

class Programacion(models.Model):
    ubicacion = models.CharField(max_length=100)
    hora_prog = models.DateTimeField()
    fecha_prog = models.DateField()
    estado = models.BooleanField()

    def __str__(self):
        return f"Programación {self.ubicacion} - {self.fecha_prog}"
