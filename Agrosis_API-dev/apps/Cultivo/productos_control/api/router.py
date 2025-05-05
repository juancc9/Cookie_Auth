from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.Cultivo.productos_control.api.views import ProductoControlViewSet

productosControlRouter = DefaultRouter()
productosControlRouter.register(prefix='productoscontrol', viewset=ProductoControlViewSet, basename='productoscontrol')

