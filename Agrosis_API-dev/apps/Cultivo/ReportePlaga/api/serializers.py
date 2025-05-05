from rest_framework import serializers
from apps.Cultivo.ReportePlaga.models import ReportePlaga
from apps.Usuarios.usuarios.api.serializer import UsuariosSerializer
from apps.Cultivo.plagas.api.serializers import PlagaSerializer
from apps.Cultivo.bancal.api.serializers import BancalSerializer
from apps.Cultivo.plagas.models import Plaga
from apps.Cultivo.bancal.models import Bancal


class ReportePlagaSerializer(serializers.ModelSerializer):
    usuario = UsuariosSerializer(read_only=True)
    plaga = PlagaSerializer(read_only=True)
    bancal = BancalSerializer(read_only=True)

    plaga_id = serializers.PrimaryKeyRelatedField(
        queryset=Plaga.objects.all(), write_only=True
    )
    bancal_id = serializers.PrimaryKeyRelatedField(
        queryset=Bancal.objects.all(), write_only=True
    )

    class Meta:
        model = ReportePlaga
        fields = [
            'id', 'usuario', 'plaga', 'plaga_id', 'bancal', 'bancal_id',
            'fecha_reporte', 'observaciones', 'estado'
        ]
        read_only_fields = ['usuario', 'fecha_reporte', 'estado']

    def create(self, validated_data):
        validated_data['plaga'] = validated_data.pop('plaga_id')
        validated_data['bancal'] = validated_data.pop('bancal_id')
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'plaga_id' in validated_data:
            validated_data['plaga'] = validated_data.pop('plaga_id')
        if 'bancal_id' in validated_data:
            validated_data['bancal'] = validated_data.pop('bancal_id')
        return super().update(instance, validated_data)
