from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from apps.Cultivo.residuos.models import Residuo
from apps.Cultivo.residuos.api.serializers import ResiduoSerializer
from apps.Usuarios.usuarios.api.permissions import IsAdminOrRead 

class ResiduoViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrRead] 
    queryset = Residuo.objects.all()
    serializer_class = ResiduoSerializer
