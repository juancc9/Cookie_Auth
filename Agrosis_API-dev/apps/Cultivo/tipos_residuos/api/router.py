from rest_framework.routers import DefaultRouter
from apps.Cultivo.tipos_residuos.api.views import TipoResiduoViewSet

tipoResiduoRouter = DefaultRouter()
tipoResiduoRouter.register(prefix='tipos_residuos', viewset=TipoResiduoViewSet, basename='tipos_residuos')

