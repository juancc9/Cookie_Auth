from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from apps.Cultivo.programacion.models import Programacion
from apps.Cultivo.programacion.api.serializers import ProgramacionSerializer
from apps.Usuarios.usuarios.api.permissions import IsAdminOrRead 

class ProgramacionViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrRead] 
    queryset = Programacion.objects.all()
    serializer_class = ProgramacionSerializer
