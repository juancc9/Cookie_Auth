from rest_framework import serializers
from apps.Cultivo.tareas.models import Tarea

class TareaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarea
        fields = '__all__'  
