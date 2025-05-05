from rest_framework import serializers
from apps.Iot.evapotranspiracion.models import Evapotranspiracion

class EvapotranspiracionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evapotranspiracion
        fields = ['id', 'fk_bancal', 'fecha', 'valor', 'creado']