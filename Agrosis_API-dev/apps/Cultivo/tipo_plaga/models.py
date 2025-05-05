from django.db import models

class TipoPlaga(models.Model):
    nombre = models.CharField(max_length=30, unique=True)
    descripcion = models.TextField()
    img = models.ImageField(upload_to='tipos_plaga_images/', null=True)

    def __str__(self):
        return self.nombre
