from rest_framework.routers import DefaultRouter
from .views import BodegaViewSet

bodegaRouter = DefaultRouter()
bodegaRouter.register(prefix='bodega', viewset=BodegaViewSet, basename='bodega')

urlpatterns = bodegaRouter.urls
