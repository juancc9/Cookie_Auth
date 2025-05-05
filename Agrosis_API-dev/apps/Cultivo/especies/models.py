from django.db import models

class Especie(models.Model):
    fk_tipo_especie = models.ForeignKey('tipo_especies.TipoEspecie', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=30, unique=True)
    descripcion = models.TextField()
    largoCrecimiento = models.IntegerField()
    img = models.ImageField(upload_to='especies_images/', null=True)

    def __str__(self):
        return self.nombre
