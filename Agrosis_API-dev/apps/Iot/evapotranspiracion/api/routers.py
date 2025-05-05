from rest_framework.routers import DefaultRouter
from apps.Iot.evapotranspiracion.api.views import EvapotranspiracionViewSet

evapotranspiracionrouter = DefaultRouter()
evapotranspiracionrouter.register(r'evapotranspiracion', EvapotranspiracionViewSet, basename='evapotranspiracion')

urlpatterns = evapotranspiracionrouter.urls