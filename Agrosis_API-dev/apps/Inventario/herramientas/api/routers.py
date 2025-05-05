from rest_framework.routers import DefaultRouter
from .views import HerramientaViewSet

herramientaRouter = DefaultRouter()
herramientaRouter.register(prefix='herramientas', viewset=HerramientaViewSet, basename='herramientas')

urlpatterns = herramientaRouter.urls