from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from apps.Iot.sensores.models import Sensor, TipoSensor
from apps.Iot.sensores.api.serializers import SensorSerializer, TipoSensorSerializer

class TipoSensorViewSet(viewsets.ModelViewSet):
    queryset = TipoSensor.objects.all()
    serializer_class = TipoSensorSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]