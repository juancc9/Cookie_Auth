from rest_framework import serializers
from apps.Cultivo.tipo_control.models import TipoControl

class TipoControlSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoControl
        fields = '__all__'
