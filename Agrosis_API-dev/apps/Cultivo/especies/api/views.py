from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from apps.Cultivo.especies.models import Especie
from apps.Cultivo.especies.api.serializers import EspecieSerializer
from apps.Usuarios.usuarios.api.permissions import IsAdminOrRead
from apps.Usuarios.usuarios.api.permissions import PermisoPorRol

class EspecieViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrRead,PermisoPorRol] 
    queryset = Especie.objects.all()
    serializer_class = EspecieSerializer
