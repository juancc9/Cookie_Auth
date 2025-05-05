from rest_framework.routers import DefaultRouter
from apps.Cultivo.tipo_plaga.api.views import TipoPlagaViewSet

tipoPlagaRouter = DefaultRouter()
tipoPlagaRouter.register(prefix='tipo_plaga', viewset=TipoPlagaViewSet, basename='tipo_plaga')

