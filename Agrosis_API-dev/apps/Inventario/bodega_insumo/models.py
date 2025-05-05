from django.db import models
from apps.Inventario.bodega.models import Bodega
from apps.Inventario.insumos.models import Insumo

class BodegaInsumo(models.Model):
    id = models.AutoField(primary_key=True)
    bodega = models.ForeignKey(Bodega, on_delete=models.CASCADE)
    insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE)
    cantidad = models.IntegerField()

    def __str__(self):
        return f'{self.bodega.nombre} - {self.insumo.nombre}'
