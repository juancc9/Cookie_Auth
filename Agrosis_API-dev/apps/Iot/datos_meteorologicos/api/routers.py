from rest_framework.routers import DefaultRouter
from apps.Iot.datos_meteorologicos.api.views import DatosMeteorologicosViewSet
 
DatosMeteorologicosRouter = DefaultRouter()
DatosMeteorologicosRouter.register(prefix='datosmeteorologicos', viewset=DatosMeteorologicosViewSet, basename='datosmeteorologicos')

urlpatterns = DatosMeteorologicosRouter.urls