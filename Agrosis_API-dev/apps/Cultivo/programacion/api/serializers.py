from rest_framework import serializers
from apps.Cultivo.programacion.models import Programacion

class ProgramacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Programacion
        fields = '__all__'
