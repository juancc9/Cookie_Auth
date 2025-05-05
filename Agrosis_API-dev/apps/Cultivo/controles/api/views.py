
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from apps.Cultivo.controles.models import Control
from apps.Cultivo.controles.api.serializers import ControlSerializer
from apps.Usuarios.usuarios.api.permissions import IsAdminOrRead 

class ControlViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrRead] 
    queryset = Control.objects.all()
    serializer_class = ControlSerializer
