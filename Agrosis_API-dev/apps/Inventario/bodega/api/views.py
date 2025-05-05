from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from apps.Usuarios.usuarios.api.permissions import PermisoPorRol
from ..models import Bodega
from .serializers import BodegaSerializer

class BodegaViewSet(viewsets.ModelViewSet):
    queryset = Bodega.objects.all()
    serializer_class = BodegaSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, PermisoPorRol]
