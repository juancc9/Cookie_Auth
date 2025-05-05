from rest_framework import serializers
from apps.Cultivo.actividades.models import Actividad, PrestamoHerramienta, PrestamoInsumo
from django.shortcuts import get_object_or_404
from apps.Usuarios.usuarios.models import Usuarios
from apps.Cultivo.actividades.api.signals import notificar_asignacion_actividad

class UsuarioActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuarios
        fields = ['nombre']  
               
class PrestamoInsumoSerializer(serializers.ModelSerializer):
    insumo_nombre = serializers.CharField(source='insumo.nombre', read_only=True)
    unidad_medida = serializers.CharField(source='insumo.unidad_medida.abreviatura', read_only=True)
    class Meta:
        model = PrestamoInsumo
        fields = '__all__'


class PrestamoHerramientaSerializer(serializers.ModelSerializer):
    herramienta_nombre = serializers.CharField(source='herramienta.nombre', read_only=True)

    class Meta:
        model = PrestamoHerramienta
        fields = '__all__'


class ActividadSerializer(serializers.ModelSerializer):
    prestamos_insumos = PrestamoInsumoSerializer(many=True, read_only=True)
    prestamos_herramientas = PrestamoHerramientaSerializer(many=True, read_only=True)
    tipo_actividad_nombre = serializers.CharField(source='tipo_actividad.nombre', read_only=True)

    usuarios = serializers.ListField(
        child=serializers.IntegerField(), write_only=True
    )
    usuarios_data = UsuarioActividadSerializer(source='usuarios', many=True, read_only=True)  

    insumos = serializers.ListField(
        child=serializers.DictField(), write_only=True, required=False
    )
    herramientas = serializers.ListField(
        child=serializers.DictField(), write_only=True, required=False
    )

    class Meta:
        model = Actividad
        fields = '__all__'
        extra_fields = ['tipo_actividad_nombre']


    def create(self, validated_data):
        usuario_ids = validated_data.pop('usuarios', [])
        insumos_data = validated_data.pop('insumos', [])
        herramientas_data = validated_data.pop('herramientas', [])

        actividad = Actividad.objects.create(**validated_data)

        from apps.Usuarios.usuarios.models import Usuarios
        usuarios = Usuarios.objects.filter(id__in=usuario_ids)
        actividad.usuarios.set(usuarios)

        from apps.Inventario.insumos.models import Insumo
        for insumo_entry in insumos_data:
            insumo = get_object_or_404(Insumo, id=insumo_entry['insumo'])
            PrestamoInsumo.objects.create(
                actividad=actividad,
                insumo=insumo,
                cantidad_usada=insumo_entry.get('cantidad_usada', 0)
            )

        from apps.Inventario.herramientas.models import Herramienta
        for herramienta_entry in herramientas_data:
            herramienta = get_object_or_404(Herramienta, id=herramienta_entry['herramienta'])
            PrestamoHerramienta.objects.create(
                actividad=actividad,
                herramienta=herramienta,
                entregada=herramienta_entry.get('entregada', True),
                devuelta=herramienta_entry.get('devuelta', False),
                fecha_devolucion=herramienta_entry.get('fecha_devolucion', None)
            )
            notificar_asignacion_actividad(actividad, usuario_ids)


        return actividad

class FinalizarActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actividad
        fields = ['fecha_fin']
        
    def validate(self, data):
        data['estado'] = 'COMPLETADA'
        if not data.get('fecha_fin'):
            raise serializers.ValidationError("La fecha de finalización es requerida")
        return data