from rest_framework.routers import DefaultRouter
from apps.Cultivo.cultivos.api.views import CultivoViewSet

cultivoRouter = DefaultRouter()
cultivoRouter.register(prefix='cultivos', viewset=CultivoViewSet, basename='cultivos')

