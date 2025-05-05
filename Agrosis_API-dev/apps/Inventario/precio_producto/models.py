from django.db import models
from django.utils import timezone

class PrecioProducto(models.Model):
    Producto = models.ForeignKey('cosechas.cosecha', on_delete=models.CASCADE, null=True, blank=True)
    unidad_medida = models.ForeignKey('insumos.UnidadMedida', on_delete=models.PROTECT, null=True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_registro = models.DateField()
    stock = models.IntegerField(default=0)
    fecha_caducidad = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.Producto} - {self.precio}"

    def save(self, *args, **kwargs):
        if self.stock < 0:
            raise ValueError("El stock no puede ser negativo.")
        if self.fecha_caducidad and self.fecha_registro and self.fecha_caducidad < self.fecha_registro:
            raise ValueError("La fecha de caducidad no puede ser anterior al registro.")
        super().save(*args, **kwargs)

    class Meta:
        db_table = "precios_productos_precio_producto"
        verbose_name = "Precio Producto"
        verbose_name_plural = "Precios Productos"