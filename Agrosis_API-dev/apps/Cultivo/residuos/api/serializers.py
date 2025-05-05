from rest_framework import serializers
from apps.Cultivo.residuos.models import Residuo

class ResiduoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Residuo
        fields = '__all__'
