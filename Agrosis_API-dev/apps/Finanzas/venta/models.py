from django.db import models

class Venta(models.Model):
    producto = models.ForeignKey('precio_producto.PrecioProducto', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    fecha = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.pk: 
            if self.cantidad <= 0:
                raise ValueError("La cantidad debe ser mayor a cero.")
            if self.cantidad > self.producto.stock:
                raise ValueError(f"Stock insuficiente. Disponible: {self.producto.stock}")
            self.total = self.producto.precio * self.cantidad
            self.producto.stock -= self.cantidad  
            self.producto.save()
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Venta de {self.producto.Producto} - {self.cantidad} {self.producto.unidad_medida} (Total: ${self.total})"