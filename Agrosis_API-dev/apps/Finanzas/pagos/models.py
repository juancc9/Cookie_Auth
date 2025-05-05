from django.db import models
from django.core.validators import MinValueValidator

class Pago(models.Model):
    actividades = models.ManyToManyField('actividades.Actividad', related_name='pagos', blank=True)
    salario = models.ForeignKey('salario.Salario', on_delete=models.PROTECT)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    horas_trabajadas = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    jornales = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    total_pago = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    fecha_calculo = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
       
        if not self.pk and not self.horas_trabajadas:
            self.horas_trabajadas = 0
            self.jornales = 0
            self.total_pago = 0
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Pago por {self.horas_trabajadas} horas (${self.total_pago})"