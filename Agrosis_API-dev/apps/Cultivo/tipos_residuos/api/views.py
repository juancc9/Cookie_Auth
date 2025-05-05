from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from apps.Cultivo.tipos_residuos.models import TipoResiduo
from apps.Cultivo.tipos_residuos.api.serializers import TipoResiduoSerializer
from apps.Usuarios.usuarios.api.permissions import IsAdminOrRead 

class TipoResiduoViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrRead] 
    queryset = TipoResiduo.objects.all()
    serializer_class = TipoResiduoSerializer
