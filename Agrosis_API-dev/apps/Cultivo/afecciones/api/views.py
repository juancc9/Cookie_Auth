from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.Cultivo.afecciones.models import Afeccion
from apps.Cultivo.afecciones.api.serializers import AfeccionSerializer
from apps.Usuarios.usuarios.api.permissions import IsAdminOrRead, PermisoPorRol

class AfeccionViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrRead, PermisoPorRol] 
    queryset = Afeccion.objects.all()
    serializer_class = AfeccionSerializer
    
    @action(detail=True, methods=['post'])
    def cambiar_estado(self, request, pk=None):
        afeccion = self.get_object()
        nuevo_estado = request.data.get('estado')
        
        if nuevo_estado not in dict(Afeccion.ESTADO_CHOICES).keys():
            return Response(
                {'error': 'Estado no válido'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        afeccion.estado = nuevo_estado
        afeccion.save()
        
        return Response(
            {'status': 'Estado actualizado'},
            status=status.HTTP_200_OK
        )
    
    def perform_create(self, serializer):
        if hasattr(self.request.user, 'tecnicoagricola'):
            serializer.save()
        else:
            serializer.save()