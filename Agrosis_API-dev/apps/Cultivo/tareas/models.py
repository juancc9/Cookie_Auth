from django.db import models

class Tarea(models.Model):
    usuario = models.ForeignKey('usuarios.Usuarios', on_delete=models.CASCADE) 
    cultivo = models.ForeignKey('cultivos.Cultivo', on_delete=models.CASCADE) 
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    fecha_inicio = models.DateField()
    fecha_limite = models.DateField()
    estado = models.BooleanField()
    prioridad = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.titulo
