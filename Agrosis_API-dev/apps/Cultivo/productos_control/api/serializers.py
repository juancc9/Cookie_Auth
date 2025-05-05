from rest_framework import serializers
from apps.Cultivo.productos_control.models import ProductoControl

class ProductoControlSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductoControl
        fields = '__all__'
