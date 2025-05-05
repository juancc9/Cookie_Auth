from django.db import models
import datetime

class Salario(models.Model):
    fecha_de_implementacion = models.DateField() 
    valorJornal = models.DecimalField(max_digits=10, decimal_places=2)
   

    def __str__(self):
        return f" Costo del jornal : {self.valorJornal} "




# Create your models here.
