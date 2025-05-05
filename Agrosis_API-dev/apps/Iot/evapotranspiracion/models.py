from django.db import models
from django.utils import timezone
from apps.Cultivo.bancal.models import Bancal

class Evapotranspiracion(models.Model):
    fk_bancal = models.ForeignKey(Bancal, on_delete=models.CASCADE, null=True)
    fecha = models.DateField()
    valor = models.DecimalField(max_digits=5, decimal_places=2)   
    creado = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Evapotranspiración para {self.fk_bancal} en {self.fecha}"

    class Meta:
        unique_together = ('fk_bancal', 'fecha')