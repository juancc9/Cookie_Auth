from rest_framework import serializers
from apps.Cultivo.plagas.models import Plaga

class PlagaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plaga
        fields = '__all__'
