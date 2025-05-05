from rest_framework import serializers
from apps.Cultivo.tipo_plaga.models import TipoPlaga

class TipoPlagaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoPlaga
        fields = '__all__'
