from django.db import models
from apps.Cultivo.cultivos.models import Cultivo

class Cosecha(models.Model):
    id_cultivo = models.ForeignKey(Cultivo, on_delete=models.CASCADE, related_name="cosechas")
    cantidad = models.IntegerField()
    unidades_de_medida = models.CharField(max_length=10)
    fecha = models.DateField()

    def __str__(self):
        return f"Cosecha {self.fecha} - {self.cantidad} {self.unidades_de_medida}"