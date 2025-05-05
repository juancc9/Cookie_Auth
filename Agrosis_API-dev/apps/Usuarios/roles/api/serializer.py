from rest_framework import serializers
from apps.Usuarios.roles.models import Roles

class RolSerializer(serializers.ModelSerializer):
    rol = serializers.CharField(source="get_nombre_display") 

    class Meta:
        model = Roles
        fields = ['id', 'rol']