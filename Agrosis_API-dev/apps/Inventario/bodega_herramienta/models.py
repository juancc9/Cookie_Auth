from django.db import models
from apps.Inventario.bodega.models import Bodega
from apps.Inventario.herramientas.models import Herramienta

class BodegaHerramienta(models.Model):
    id = models.AutoField(primary_key=True)
    bodega = models.ForeignKey(Bodega, on_delete=models.CASCADE, related_name="bodegas_herramientas")
    herramienta = models.ForeignKey(Herramienta, on_delete=models.CASCADE, related_name="herramientas_bodegas")
    cantidad = models.PositiveIntegerField(default=1) 

    def __str__(self):
        return f'{self.bodega.nombre if self.bodega else "Sin Bodega"} - {self.herramienta.nombre if self.herramienta else "Sin Herramienta"}'
