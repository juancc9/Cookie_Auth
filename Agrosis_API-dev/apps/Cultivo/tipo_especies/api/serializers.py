from rest_framework import serializers
from apps.Cultivo.tipo_especies.models import TipoEspecie

class TipoEspecieSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoEspecie
        fields = '__all__'
