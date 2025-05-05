from rest_framework.routers import DefaultRouter
from apps.Cultivo.cosechas.api.views import CosechaViewSet

cosechaRouter = DefaultRouter()
cosechaRouter.register(prefix='cosechas', viewset=CosechaViewSet, basename='cosechas')

