from django.db import models

class Lote(models.Model):
    nombre = models.CharField(max_length=15, unique=True)
    descripcion = models.TextField(null=True, blank=True)
    activo = models.BooleanField()
    tam_x = models.DecimalField(max_digits=3, decimal_places=2)
    tam_y = models.DecimalField(max_digits=3, decimal_places=2)
    pos_y = models.DecimalField(max_digits=3, decimal_places=2)
    pos_x = models.DecimalField(max_digits=3, decimal_places=2)

    def __str__(self):
        return self.nombre
