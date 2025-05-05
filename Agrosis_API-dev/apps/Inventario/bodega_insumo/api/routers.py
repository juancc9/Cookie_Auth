from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import BodegaInsumoViewSet

bodegaInsumoRouter = DefaultRouter()
bodegaInsumoRouter.register(prefix='bodega_insumo', viewset=BodegaInsumoViewSet, basename='bodega_insumo')

urlpatterns = bodegaInsumoRouter.urls + [
    path('bodega_insumo/reporte_pdf/', BodegaInsumoViewSet.as_view({'get': 'reporte_pdf'}), name='bodega_insumo_reporte_pdf'),
]
