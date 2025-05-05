from django.db import models

class Residuo(models.Model):
    id_cultivo = models.ForeignKey('cultivos.Cultivo', on_delete=models.CASCADE, related_name="residuos")
    id_tipo_residuo = models.ForeignKey('tipos_residuos.TipoResiduo', on_delete=models.CASCADE, related_name="residuos")
    nombre = models.CharField(max_length=30, unique=True)
    descripcion = models.TextField(null=True, blank=True)
    fecha = models.DateField()
    cantidad = models.IntegerField()

    def __str__(self):
        return self.nombre
