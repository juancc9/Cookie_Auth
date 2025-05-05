from rest_framework import serializers
from apps.Cultivo.bancal.models import Bancal

class BancalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bancal
        fields = '__all__'
