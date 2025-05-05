from rest_framework.routers import DefaultRouter
from .views import PrecioProductoViewSet

precioProductoRouter = DefaultRouter()
precioProductoRouter.register(prefix='precio-producto', viewset=PrecioProductoViewSet, basename='precio-producto')

urlpatterns = precioProductoRouter.urls