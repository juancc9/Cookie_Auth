from rest_framework.routers import DefaultRouter
from apps.Cultivo.tipo_especies.api.views import TipoEspecieViewSet

tipoEspecieRouter = DefaultRouter()
tipoEspecieRouter.register(prefix='tipo_especies', viewset=TipoEspecieViewSet, basename='tipo_especies')

