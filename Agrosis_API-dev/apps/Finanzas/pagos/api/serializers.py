from rest_framework import serializers
from apps.Finanzas.pagos.models import Pago
from apps.Cultivo.actividades.models import Actividad
from apps.Finanzas.salario.models import Salario
from django.core.exceptions import ValidationError

class PagoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pago
        fields = ['fecha_inicio', 'fecha_fin']
        
class PagoSerializer(serializers.ModelSerializer):
    nombre_usuario = serializers.SerializerMethodField()

    class Meta:
        model = Pago
        fields = '__all__'
        read_only_fields = ['horas_trabajadas', 'jornales', 'total_pago', 'fecha_calculo', 'salario', 'actividades']

    def get_nombre_usuario(self, obj):
        usuarios = set()

        actividades = obj.actividades.all() if hasattr(obj, 'actividades') else []
        print(f"01 {getattr(obj, 'id', 'N/A')}: {actividades}")

        for actividad in actividades:
            try:
                for usuario in actividad.usuarios.all():
                    usuarios.add(usuario.nombre)
            except Exception as e:
                print(f"Error accediendo a usuarios de la actividad {actividad.id}: {e}")

        return ', '.join(usuarios) if usuarios else 'Desconocido'


class CalculoPagoSerializer(serializers.Serializer):
    usuario_id = serializers.IntegerField()
    fecha_inicio = serializers.DateField()
    fecha_fin = serializers.DateField()





    def validate(self, data):
        if data['fecha_inicio'] > data['fecha_fin']:
            raise serializers.ValidationError("La fecha de inicio no puede ser mayor que la fecha fin")
        return data

    def create(self, validated_data):
        usuario_id = validated_data['usuario_id']
        fecha_inicio = validated_data['fecha_inicio']
        fecha_fin = validated_data['fecha_fin']

        actividades = Actividad.objects.filter(
            usuarios__id=usuario_id,
            estado='COMPLETADA',
            fecha_fin__date__gte=fecha_inicio,
            fecha_fin__date__lte=fecha_fin
        )

        if not actividades.exists():
            raise ValidationError("No hay actividades completadas en el rango especificado")

        total_segundos = sum(
            (act.fecha_fin - act.fecha_inicio).total_seconds()
            for act in actividades
        )
        horas_trabajadas = total_segundos / 3600

        salario = Salario.objects.order_by('-fecha_de_implementacion').first()
        if not salario:
            raise ValidationError("No existe un valor de jornal configurado")

        jornales = horas_trabajadas / 8.5
        total_pago = jornales * float(salario.valorJornal)

        pago = Pago.objects.create(
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            horas_trabajadas=round(horas_trabajadas, 2),
            jornales=round(jornales, 2),
            total_pago=round(total_pago, 2),
            salario=salario
        )
        pago.actividades.set(actividades)
        
        return pago