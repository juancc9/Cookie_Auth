from rest_framework import serializers
from ..models import BodegaHerramienta, Bodega, Herramienta

class BodegaHerramientaSerializer(serializers.ModelSerializer):
    bodega = serializers.PrimaryKeyRelatedField(queryset=Bodega.objects.all())
    herramienta = serializers.PrimaryKeyRelatedField(queryset=Herramienta.objects.all())

    class Meta:
        model = BodegaHerramienta
        fields = '__all__'