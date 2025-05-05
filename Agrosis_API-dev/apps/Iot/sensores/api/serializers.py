from rest_framework import serializers
from apps.Iot.sensores.models import Sensor, TipoSensor

class TipoSensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoSensor
        fields = '__all__'

class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ['id', 'nombre', 'tipo_sensor', 'unidad_medida', 'descripcion']