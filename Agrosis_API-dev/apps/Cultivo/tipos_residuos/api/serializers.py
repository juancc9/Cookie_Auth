from rest_framework import serializers
from apps.Cultivo.tipos_residuos.models import TipoResiduo

class TipoResiduoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoResiduo
        fields = '__all__'
