from django.db import models

class Semillero(models.Model):
    fk_especie = models.ForeignKey('especies.Especie', on_delete=models.CASCADE)
    unidades_de_medida = models.IntegerField()
    fechaSiembra = models.DateField()
    fechaEstimada = models.DateField()
    img = models.ImageField(upload_to='semilleros_images/', null=True, blank=True)

    def __str__(self):
        return f'Semillero {self.fk_especie.nombre}'
