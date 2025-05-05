from rest_framework.routers import DefaultRouter
from apps.Cultivo.tipo_control.api.views import TipoControlViewSet

tipoControlRouter = DefaultRouter()
tipoControlRouter.register(prefix='tipo_control', viewset=TipoControlViewSet, basename='tipo_control')

