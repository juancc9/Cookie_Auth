from rest_framework.routers import DefaultRouter
from apps.Cultivo.residuos.api.views import ResiduoViewSet

residuosRouter = DefaultRouter()
residuosRouter.register(prefix='residuos', viewset=ResiduoViewSet, basename='residuos')
