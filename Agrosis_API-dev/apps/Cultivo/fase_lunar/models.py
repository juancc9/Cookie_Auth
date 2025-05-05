from django.db import models

class FaseLunar(models.Model):
    nombre = models.CharField(max_length=30)
    fase_lunar = models.CharField(max_length=30)
    descripcion = models.TextField()
    recomendaciones = models.TextField()
    fecha = models.DateField()
    img = models.ImageField(upload_to='fases_lunares_images/', null=True, blank=True)

    def __str__(self):
        return self.nombre
