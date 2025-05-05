from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from apps.Cultivo.semillero.models import Semillero
from apps.Cultivo.semillero.api.serializers import SemilleroSerializer
from apps.Usuarios.usuarios.api.permissions import IsAdminOrRead 

class SemilleroViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrRead] 
    queryset = Semillero.objects.all()
    serializer_class = SemilleroSerializer
