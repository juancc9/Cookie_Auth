from rest_framework import serializers
from ..models import Insumo, UnidadMedida, TipoInsumo, InsumoCompuesto
from django.utils import timezone

class UnidadMedidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadMedida
        fields = ['id', 'nombre', 'descripcion', 'fecha_creacion', 'creada_por_usuario']

class TipoInsumoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoInsumo
        fields = ['id', 'nombre', 'descripcion', 'fecha_creacion', 'creada_por_usuario']

class InsumoCompuestoSerializer(serializers.ModelSerializer):
    insumo_componente = serializers.PrimaryKeyRelatedField(
        queryset=Insumo.objects.all()
    )
    cantidad = serializers.FloatField(min_value=0.01, error_messages={
        'min_value': 'La cantidad debe ser mayor a 0.'
    })

    class Meta:
        model = InsumoCompuesto
        fields = ['insumo_componente', 'cantidad']

    def validate_insumo_componente(self, value):
        insumo_id = self.context.get('insumo_id')
        if insumo_id and value.id == insumo_id:
            raise serializers.ValidationError("Un insumo no puede ser su propio componente.")
        return value

class InsumoSerializer(serializers.ModelSerializer):
    unidad_medida = UnidadMedidaSerializer(read_only=True)
    tipo_insumo = TipoInsumoSerializer(read_only=True)
    unidad_medida_id = serializers.PrimaryKeyRelatedField(
        queryset=UnidadMedida.objects.all(),
        write_only=True,
        allow_null=True
    )
    tipo_insumo_id = serializers.PrimaryKeyRelatedField(
        queryset=TipoInsumo.objects.all(),
        write_only=True,
        allow_null=True
    )
    componentes = InsumoCompuestoSerializer(many=True, read_only=True)
    componentes_data = InsumoCompuestoSerializer(many=True, write_only=True, required=False)

    class Meta:
        model = Insumo
        fields = [
            'id', 'nombre', 'descripcion', 'cantidad', 'unidad_medida', 'unidad_medida_id',
            'tipo_insumo', 'tipo_insumo_id', 'activo', 'tipo_empacado', 'fecha_registro',
            'fecha_caducidad', 'precio_insumo', 'es_compuesto', 'componentes', 'componentes_data'
        ]

    def validate_nombre(self, value):
        if not value.strip():
            raise serializers.ValidationError("El nombre es requerido.")
        return value

    def validate_descripcion(self, value):
        if not value.strip():
            raise serializers.ValidationError("La descripción es requerida.")
        return value

    def validate_cantidad(self, value):
        if value < 0:
            raise serializers.ValidationError("La cantidad no puede ser negativa.")
        return value

    def validate_componentes_data(self, value):
        if not self.initial_data.get('es_compuesto', False) and value:
            raise serializers.ValidationError("No se pueden asignar componentes a un insumo no compuesto.")
        if self.initial_data.get('es_compuesto', False) and not value:
            raise serializers.ValidationError("Se requieren componentes para un insumo compuesto.")
        return value

    def validate(self, data):
        return data

    def create(self, validated_data):
        componentes_data = validated_data.pop('componentes_data', [])
        unidad_medida = validated_data.pop('unidad_medida_id', None)
        tipo_insumo = validated_data.pop('tipo_insumo_id', None)
        validated_data['fecha_registro'] = timezone.now()

        insumo = Insumo.objects.create(
            unidad_medida=unidad_medida,
            tipo_insumo=tipo_insumo,
            **validated_data
        )

        for componente_data in componentes_data:
            InsumoCompuesto.objects.create(
                insumo_compuesto=insumo,
                insumo_componente=componente_data['insumo_componente'],
                cantidad=componente_data['cantidad']
            )

        return insumo

    def update(self, instance, validated_data):
        componentes_data = validated_data.pop('componentes_data', None)
        unidad_medida = validated_data.pop('unidad_medida_id', None)
        tipo_insumo = validated_data.pop('tipo_insumo_id', None)

        if unidad_medida is not None:
            instance.unidad_medida = unidad_medida
        if tipo_insumo is not None:
            instance.tipo_insumo = tipo_insumo

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if componentes_data is not None:
            instance.componentes.all().delete()
            for componente_data in componentes_data:
                InsumoCompuesto.objects.create(
                    insumo_compuesto=instance,
                    insumo_componente=componente_data['insumo_componente'],
                    cantidad=componente_data['cantidad']
                )

        return instance