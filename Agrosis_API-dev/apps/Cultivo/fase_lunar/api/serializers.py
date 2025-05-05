from rest_framework import serializers
from apps.Cultivo.fase_lunar.models import FaseLunar

class FaseLunarSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaseLunar
        fields = '__all__'
