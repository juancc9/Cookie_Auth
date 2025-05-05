from rest_framework import serializers
from apps.Cultivo.cultivos.models import Cultivo

class CultivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cultivo
        fields = '__all__'
