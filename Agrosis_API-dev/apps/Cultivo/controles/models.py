from django.db import models


class Control(models.Model):
    afeccion = models.ForeignKey('afecciones.Afeccion', on_delete=models.CASCADE)
    tipo_control = models.ForeignKey('tipo_control.TipoControl', on_delete=models.CASCADE)
    producto = models.ForeignKey('productos_control.ProductoControl', on_delete=models.CASCADE)
    descripcion = models.TextField()
    fecha_control = models.DateField()
    responsable = models.ForeignKey('usuarios.Usuarios', on_delete=models.SET_NULL, null=True)
    efectividad = models.PositiveSmallIntegerField(
        choices=[(i, f"{i}%") for i in range(0, 101, 10)],
        default=50
    )
    observaciones = models.TextField(blank=True)

    def __str__(self):
        return f'{self.afeccion.nombre} - {self.producto.nombre}'