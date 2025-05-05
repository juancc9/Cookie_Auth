from rest_framework import serializers
from apps.Cultivo.controles.models import Control
from apps.Cultivo.afecciones.api.serializers import AfeccionSerializer
from apps.Cultivo.afecciones.models import Afeccion

from apps.Cultivo.productos_control.api.serializers import ProductoControlSerializer
from apps.Cultivo.productos_control.models import ProductoControl

from apps.Cultivo.tipo_control.api.serializers import TipoControlSerializer
from apps.Cultivo.tipo_control.models import TipoControl

from apps.Usuarios.usuarios.api.serializer import UsuariosSerializer
from apps.Usuarios.usuarios.models import Usuarios


class ControlSerializer(serializers.ModelSerializer):
    afeccion = AfeccionSerializer(read_only=True)
    afeccion_id = serializers.PrimaryKeyRelatedField(
        queryset=Afeccion.objects.all(),
        source='afeccion',
        write_only=True
    )
    producto = ProductoControlSerializer(read_only=True)
    producto_id = serializers.PrimaryKeyRelatedField(
        queryset=ProductoControl.objects.all(),
        source='producto',
        write_only=True
    )
    tipo_control = TipoControlSerializer(read_only=True)
    tipo_control_id = serializers.PrimaryKeyRelatedField(
        queryset=TipoControl.objects.all(),
        source='tipo_control',
        write_only=True
    )
    responsable = UsuariosSerializer(read_only=True)
    responsable_id = serializers.PrimaryKeyRelatedField(
        queryset=Usuarios.objects.all(),
        source='responsable',
        write_only=True
    )
    
    class Meta:
        model = Control
        fields = [
            'id', 'afeccion', 'afeccion_id', 'tipo_control', 'tipo_control_id',
            'producto', 'producto_id', 'descripcion', 'fecha_control',
            'responsable', 'responsable_id', 'efectividad', 'observaciones'
        ]