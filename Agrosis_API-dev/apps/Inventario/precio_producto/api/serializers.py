from rest_framework import serializers
from ..models import PrecioProducto
from apps.Inventario.insumos.models import UnidadMedida
from apps.Cultivo.cosechas.models import Cosecha

class UnidadMedidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadMedida
        fields = ['id', 'nombre', 'descripcion', 'creada_por_usuario', 'fecha_creacion']

class PrecioProductoSerializer(serializers.ModelSerializer):
    unidad_medida = UnidadMedidaSerializer(read_only=True)
    unidad_medida_id = serializers.PrimaryKeyRelatedField(
        queryset=UnidadMedida.objects.all(),
        source='unidad_medida',
        write_only=True,
        allow_null=True
    )
    Producto = serializers.StringRelatedField(read_only=True)
    Producto_id = serializers.PrimaryKeyRelatedField(
        source='Producto',
        queryset=Cosecha.objects.all(),
        allow_null=True,
        required=False
    )

    class Meta:
        model = PrecioProducto
        fields = ['id', 'Producto', 'Producto_id', 'unidad_medida', 'unidad_medida_id', 'precio', 'fecha_registro', 'stock', 'fecha_caducidad']