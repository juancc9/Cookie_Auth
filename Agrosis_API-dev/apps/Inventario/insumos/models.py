from django.db import models
from django.utils import timezone


class UnidadMedida(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    creada_por_usuario = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Unidad de Medida"
        verbose_name_plural = "Unidades de Medida"
        db_table = "unidad_medida_unidadmedida"


class TipoInsumo(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    creada_por_usuario = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Tipo de Insumo"
        verbose_name_plural = "Tipos de Insumos"
        db_table = "insumos_tiposinsumo"


class Insumo(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    cantidad = models.IntegerField()
    unidad_medida = models.ForeignKey(
        UnidadMedida,
        on_delete=models.PROTECT,
        related_name="insumos",
        null=True,
        blank=True,
    )
    tipo_insumo = models.ForeignKey(
        "TipoInsumo",
        on_delete=models.PROTECT,
        related_name="insumos",
        null=True,
        blank=True,
    )
    activo = models.BooleanField(default=True)
    tipo_empacado = models.CharField(max_length=100, blank=True, null=True)
    fecha_registro = models.DateTimeField(default=timezone.now)
    fecha_caducidad = models.DateField(blank=True, null=True)
    precio_insumo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    es_compuesto = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = "insumos_insumo"


class InsumoCompuesto(models.Model):
    id = models.AutoField(primary_key=True)
    insumo_compuesto = models.ForeignKey(
        Insumo,
        on_delete=models.CASCADE,
        related_name="componentes",
    )
    insumo_componente = models.ForeignKey(
        Insumo,
        on_delete=models.PROTECT,
        related_name="usado_en_compuestos",
    )
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "insumos_insumocompuesto"
        unique_together = ("insumo_compuesto", "insumo_componente")
        verbose_name = "Insumo Compuesto"
        verbose_name_plural = "Insumos Compuestos"

    def __str__(self):
        return f"{self.insumo_componente.nombre} en {self.insumo_compuesto.nombre}"