from rest_framework import serializers
from apps.Cultivo.semillero.models import Semillero

class SemilleroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semillero
        fields = '__all__'
