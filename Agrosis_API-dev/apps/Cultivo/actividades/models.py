from django.db import models

class Actividad(models.Model):
    
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('EN_PROCESO', 'En proceso'),
        ('COMPLETADA', 'Completada'),
        ('CANCELADA', 'Cancelada'),
    ]

    tipo_actividad = models.ForeignKey('tipo_actividad.TipoActividad', on_delete=models.CASCADE)
    descripcion = models.TextField()
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    cultivo = models.ForeignKey('cultivos.Cultivo', on_delete=models.CASCADE)
    
    usuarios = models.ManyToManyField('usuarios.Usuarios', related_name='actividades')
    
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='PENDIENTE'
    )
    prioridad = models.CharField(
        max_length=20,
        choices=[('ALTA', 'Alta'), ('MEDIA', 'Media'), ('BAJA', 'Baja')],
        default='MEDIA'
    )
    instrucciones_adicionales = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.tipo_actividad} - {self.estado}"
    
class PrestamoInsumo(models.Model):
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE, related_name='prestamos_insumos')
    insumo = models.ForeignKey('insumos.Insumo', on_delete=models.CASCADE)
    cantidad_usada = models.IntegerField(default=0)
    cantidad_devuelta = models.IntegerField(default=0)
    fecha_devolucion = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.insumo.nombre} prestado a {self.actividad}"


class PrestamoHerramienta(models.Model):
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE, related_name='prestamos_herramientas')
    herramienta = models.ForeignKey('herramientas.Herramienta', on_delete=models.CASCADE)
    entregada = models.BooleanField(default=True)
    devuelta = models.BooleanField(default=False)
    fecha_devolucion = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.herramienta.nombre} prestada a {self.actividad}"

