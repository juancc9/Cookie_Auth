from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from apps.Cultivo.productos_control.models import ProductoControl
from apps.Cultivo.productos_control.api.serializers import ProductoControlSerializer
from apps.Usuarios.usuarios.api.permissions import IsAdminOrRead,PermisoPorRol

class ProductoControlViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrRead,PermisoPorRol] 
    queryset = ProductoControl.objects.all()
    serializer_class = ProductoControlSerializer
