from rest_framework.routers import DefaultRouter
from apps.Cultivo.plantaciones.api.views import PlantacionViewSet

plantacionRouter = DefaultRouter()
plantacionRouter.register(prefix='plantaciones', viewset=PlantacionViewSet, basename='platantaciones')

