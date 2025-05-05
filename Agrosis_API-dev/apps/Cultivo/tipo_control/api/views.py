from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from apps.Cultivo.tipo_control.models import TipoControl
from apps.Cultivo.tipo_control.api.serializers import TipoControlSerializer
from apps.Usuarios.usuarios.api.permissions import IsAdminOrRead 

class TipoControlViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrRead] 
    queryset = TipoControl.objects.all()
    serializer_class = TipoControlSerializer
