from django.db import models

class ReportePlaga(models.Model):
    usuario = models.ForeignKey('usuarios.Usuarios', on_delete=models.CASCADE)
    plaga = models.ForeignKey('plagas.Plaga', on_delete=models.CASCADE)
    bancal = models.ForeignKey('bancal.Bancal', on_delete=models.CASCADE)
    fecha_reporte = models.DateTimeField(auto_now_add=True)
    observaciones = models.TextField()
    estado = models.CharField(max_length=2, choices=[
        ('PE', 'Pendiente'),
        ('RE', 'Revisado'),
        ('AT', 'Atendido')
    ], default='PE')

    def __str__(self):
        return f"Reporte {self.id} - {self.plaga.nombre}"