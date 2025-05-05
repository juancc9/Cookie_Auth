from rest_framework import serializers
from apps.Cultivo.afecciones.models import Afeccion
from apps.Cultivo.plagas.api.serializers import PlagaSerializer
from apps.Cultivo.plagas.models import Plaga

from apps.Cultivo.cultivos.api.serializers import CultivoSerializer
from apps.Cultivo.cultivos.models import Cultivo

from apps.Cultivo.bancal.api.serializers import BancalSerializer
from apps.Cultivo.bancal.models import Bancal


class AfeccionSerializer(serializers.ModelSerializer):
    plaga = PlagaSerializer(read_only=True)
    plaga_id = serializers.PrimaryKeyRelatedField(
        queryset=Plaga.objects.all(), 
        source='plaga',
        write_only=True
    )
    cultivo = CultivoSerializer(read_only=True)
    cultivo_id = serializers.PrimaryKeyRelatedField(
        queryset=Cultivo.objects.all(), 
        source='cultivo',
        write_only=True
    )
    bancal = BancalSerializer(read_only=True)
    bancal_id = serializers.PrimaryKeyRelatedField(
        queryset=Bancal.objects.all(), 
        source='bancal',
        write_only=True
    )
    
    class Meta:
        model = Afeccion
        fields = [
            'id', 'reporte', 'nombre', 'descripcion', 'fecha_deteccion',
            'gravedad', 'estado', 'plaga', 'plaga_id', 'cultivo', 'cultivo_id',
            'bancal', 'bancal_id'
        ]
        read_only_fields = ['estado']