from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from apps.Cultivo.plantaciones.models import Plantacion
from apps.Cultivo.plantaciones.api.serializers import PlantacionSerializer
from apps.Usuarios.usuarios.api.permissions import IsAdminOrRead 

class PlantacionViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrRead] 
    queryset = Plantacion.objects.all()
    serializer_class = PlantacionSerializer
