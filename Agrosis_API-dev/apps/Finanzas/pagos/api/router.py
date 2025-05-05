from rest_framework.routers import DefaultRouter
from apps.Finanzas.pagos.api.views import PagoViewSet


pagoRouter = DefaultRouter()
pagoRouter.register(prefix='pago', viewset=PagoViewSet, basename='pago')