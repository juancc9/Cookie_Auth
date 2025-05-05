from django.db import models
class Cultivo(models.Model):
    Especie = models.ForeignKey('especies.Especie', on_delete=models.CASCADE)
    Bancal = models.ForeignKey('bancal.Bancal', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50, unique=True)
    unidad_de_medida = models.CharField(max_length=10, null=True)
    activo = models.BooleanField()
    fechaSiembra = models.DateField()

    def __str__(self):
        return self.nombre
