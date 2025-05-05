from rest_framework.routers import DefaultRouter
from  apps.Finanzas.venta.api.views import VentaViewSet

ventaRouter = DefaultRouter()
ventaRouter.register(prefix='venta', viewset=VentaViewSet, basename='venta')