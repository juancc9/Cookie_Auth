from rest_framework.routers import DefaultRouter
from apps.Cultivo.tipo_actividad.api.views import TipoActividadViewSet

tipoActividadRouter = DefaultRouter()
tipoActividadRouter.register(prefix='tipo_actividad', viewset=TipoActividadViewSet, basename='tipo_actividad')

