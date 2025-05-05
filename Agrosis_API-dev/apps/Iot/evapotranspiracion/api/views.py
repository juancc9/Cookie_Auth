from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from apps.Iot.evapotranspiracion.models import Evapotranspiracion
from apps.Iot.evapotranspiracion.api.serializers import EvapotranspiracionSerializer
from apps.Iot.evapotranspiracion.utils import calcular_evapotranspiracion_diaria
from datetime import datetime

class EvapotranspiracionViewSet(viewsets.ModelViewSet):
    queryset = Evapotranspiracion.objects.all()
    serializer_class = EvapotranspiracionSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['fk_bancal_id', 'fecha']

    def get_permissions(self):
        if self.action in ['create', 'calcular']:
            return [AllowAny()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['post'])
    def calcular(self, request):
        """
        Calcula la evapotranspiración para un bancal y fecha específica.
        Ejemplo de solicitud:
        {
            "fk_bancal_id": 1,
            "fecha": "2023-10-01",
            "latitud": 4.61,
            "altitud": 2600
        }
        """
        fk_bancal_id = request.data.get('fk_bancal_id')
        fecha_str = request.data.get('fecha')
        latitud = float(request.data.get('latitud', 0))
        altitud = float(request.data.get('altitud', 0))

        try:
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        except ValueError:
            return Response({"error": "Formato de fecha inválido. Use YYYY-MM-DD."}, status=400)

        ETo = calcular_evapotranspiracion_diaria(fk_bancal_id, fecha, latitud, altitud)
        if ETo is None:
            return Response({"error": "No hay datos suficientes para calcular la evapotranspiración."}, status=400)

        evapotranspiracion, created = Evapotranspiracion.objects.update_or_create(
            fk_bancal_id=fk_bancal_id,
            fecha=fecha,
            defaults={'valor': ETo}
        )

        serializer = self.get_serializer(evapotranspiracion)
        return Response(serializer.data, status=201 if created else 200)