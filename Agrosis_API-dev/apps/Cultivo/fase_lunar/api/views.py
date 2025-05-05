from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from apps.Cultivo.fase_lunar.models import FaseLunar
from apps.Cultivo.fase_lunar.api.serializers import FaseLunarSerializer
from apps.Usuarios.usuarios.api.permissions import IsAdminOrRead 

class FaseLunarViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrRead] 
    queryset = FaseLunar.objects.all()
    serializer_class = FaseLunarSerializer
