from rest_framework import serializers
from apps.Cultivo.tipo_actividad.models import TipoActividad

class TipoActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoActividad
        fields = '__all__'
