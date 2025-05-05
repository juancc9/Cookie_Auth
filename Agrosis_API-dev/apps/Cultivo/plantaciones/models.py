from django.db import models

class Plantacion(models.Model):
    id_cultivo = models.ForeignKey('cultivos.Cultivo', on_delete=models.CASCADE)
    bancal = models.ForeignKey('bancal.Bancal', on_delete=models.CASCADE)

    def __str__(self):
        return f'Plantación {self.id_cultivo.nombre}'
