from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from apps.Cultivo.tipo_actividad.models import TipoActividad
from apps.Cultivo.tipo_actividad.api.serializers import TipoActividadSerializer
from apps.Usuarios.usuarios.api.permissions import IsAdminOrRead 
from apps.Usuarios.usuarios.api.permissions import PermisoPorRol
from apps.Usuarios.usuarios.models import Usuarios


class TipoActividadViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrRead, PermisoPorRol] 
    queryset = TipoActividad.objects.all()
    serializer_class = TipoActividadSerializer
