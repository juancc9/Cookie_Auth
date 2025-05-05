from django.db import models
class Bancal(models.Model):
    nombre = models.CharField(max_length=15, unique=True)
    TamX = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    TamY = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    posY = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    posX = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    lote = models.ForeignKey('lotes.Lote', on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre