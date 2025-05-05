from rest_framework import serializers
from apps.Cultivo.cosechas.models import Cosecha

class CosechaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cosecha
        fields = '__all__'
