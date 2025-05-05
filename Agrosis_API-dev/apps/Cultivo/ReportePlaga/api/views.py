from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.Cultivo.ReportePlaga.models import ReportePlaga
from apps.Cultivo.ReportePlaga.api.serializers import ReportePlagaSerializer
from apps.Usuarios.usuarios.api.permissions import IsAdminOrRead, PermisoPorRol

class ReportePlagaViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrRead, PermisoPorRol] 
    queryset = ReportePlaga.objects.all()
    serializer_class = ReportePlagaSerializer
    
    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

    @action(detail=True, methods=['post'])
    def revisar(self, request, pk=None):
        reporte = self.get_object()
        reporte.estado = 'RE'
        reporte.save()
        return Response({'status': 'Reporte marcado como revisado'})
    
    @action(detail=True, methods=['post'])
    def atender(self, request, pk=None):
        reporte = self.get_object()
        reporte.estado = 'AT'
        reporte.save()
        return Response({'status': 'Reporte marcado como atendido'})
