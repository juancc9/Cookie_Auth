from django.db import models


class Afeccion(models.Model):
    reporte = models.ForeignKey('ReportePlaga.ReportePlaga', on_delete=models.SET_NULL, null=True, blank=True)
    cultivo = models.ForeignKey('cultivos.Cultivo', on_delete=models.CASCADE)
    plaga = models.ForeignKey('plagas.Plaga', on_delete=models.CASCADE)
    bancal = models.ForeignKey('bancal.Bancal', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=30)
    descripcion = models.TextField()
    fecha_deteccion = models.DateField()
    gravedad = models.CharField(max_length=1, choices=[
        ('L', 'Leve'),
        ('M', 'Moderada'),
        ('G', 'Grave')
    ])
    estado = models.CharField(max_length=2, choices=[
        ('ST', 'Estable'), 
        ('EC', 'En Control'), 
        ('EL', 'Eliminada'),
        ('AC', 'Activa')
    ], default='AC')

    def __str__(self):
        return self.nombre