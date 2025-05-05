from rest_framework import serializers
from ..models import BodegaInsumo

class BodegaInsumoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BodegaInsumo
        fields = '__all__'
