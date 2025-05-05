from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from apps.Cultivo.tareas.models import Tarea
from apps.Cultivo.tareas.api.serializers import TareaSerializer
from apps.Usuarios.usuarios.api.permissions import IsAdminOrRead 

class TareaViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrRead]  
    queryset = Tarea.objects.all()
    serializer_class = TareaSerializer
