from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated 
from rest_framework import viewsets
from apps.Finanzas.salario.models import Salario
from apps.Finanzas.salario.api.serializers import SalarioSerializer
from apps.Usuarios.usuarios.api.permissions import IsAdminOrRead, PermisoPorRol

class SalarioViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrRead, PermisoPorRol]
    queryset = Salario.objects.all()
    serializer_class = SalarioSerializer
    def perform_create(self, serializer):
        serializer.save()
