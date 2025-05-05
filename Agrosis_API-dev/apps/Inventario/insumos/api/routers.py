from rest_framework.routers import DefaultRouter
from .views import InsumoViewSet

insumoRouter = DefaultRouter()
insumoRouter.register(prefix='insumo', viewset=InsumoViewSet, basename='insumo')

urlpatterns = insumoRouter.urls