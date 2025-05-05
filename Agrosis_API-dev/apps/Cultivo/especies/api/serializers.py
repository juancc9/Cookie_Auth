from rest_framework import serializers
from apps.Cultivo.especies.models import Especie

class EspecieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especie
        fields = '__all__'
