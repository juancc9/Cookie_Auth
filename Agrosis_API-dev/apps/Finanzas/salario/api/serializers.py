from rest_framework import serializers
from apps.Finanzas.salario.models import Salario

class SalarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salario
        fields = '__all__'
