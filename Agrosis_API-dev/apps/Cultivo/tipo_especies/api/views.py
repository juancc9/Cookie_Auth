from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from apps.Cultivo.tipo_especies.models import TipoEspecie
from apps.Cultivo.tipo_especies.api.serializers import TipoEspecieSerializer
from apps.Usuarios.usuarios.api.permissions import IsAdminOrRead 
from apps.Usuarios.usuarios.api.permissions import PermisoPorRol

class TipoEspecieViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrRead, PermisoPorRol] 
    queryset = TipoEspecie.objects.all()
    serializer_class = TipoEspecieSerializer
