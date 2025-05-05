from rest_framework.routers import DefaultRouter
from apps.Iot.sensores.api.views import SensorViewSet, TipoSensorViewSet

SensoresRouter = DefaultRouter()
SensoresRouter.register(r'sensores', SensorViewSet, basename='sensores')  
SensoresRouter.register(r'tiposensor', TipoSensorViewSet, basename='tiposensor')