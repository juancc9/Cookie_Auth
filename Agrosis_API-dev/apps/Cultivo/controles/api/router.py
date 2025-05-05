from rest_framework.routers import DefaultRouter
from .views import ControlViewSet

controlRouter = DefaultRouter()
controlRouter.register(prefix='control', viewset=ControlViewSet, basename='control')
