from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import BodegaHerramientaViewSet

bodegaHerramientaRouter = DefaultRouter()
bodegaHerramientaRouter.register(prefix='bodega_herramienta', viewset=BodegaHerramientaViewSet, basename='bodega_herramienta')

urlpatterns = [
    path('bodega_herramienta/reporte_pdf/', BodegaHerramientaViewSet.as_view({'get': 'reporte_pdf'}), name='reporte-herramientas'),
]

urlpatterns += bodegaHerramientaRouter.urls
