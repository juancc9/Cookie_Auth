from rest_framework import serializers
from apps.Iot.datos_meteorologicos.models import Datos_metereologicos

class Datos_metereologicosSerializer(serializers.ModelSerializer):
    sensor_nombre = serializers.CharField(source='fk_sensor.nombre', read_only=True, default='N/A')
    bancal_nombre = serializers.CharField(source='fk_bancal.nombre', read_only=True, default='N/A')

    class Meta:
        model = Datos_metereologicos
        fields = [
            'id', 'fk_sensor', 'sensor_nombre', 'fk_bancal', 'bancal_nombre', 
            'temperatura', 'humedad_ambiente', 'luminosidad', 'lluvia', 
            'velocidad_viento', 'direccion_viento', 'humedad_suelo', 'ph_suelo', 
            'fecha_medicion'
        ]
 