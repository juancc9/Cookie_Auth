from django.db import models

class TipoControl(models.Model):
    nombre = models.CharField(max_length=30, unique=True)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre
