from rest_framework.routers import DefaultRouter
from apps.Cultivo.plagas.api.views import PlagaViewSet

plagasRouter = DefaultRouter()
plagasRouter.register(prefix='plaga', viewset=PlagaViewSet, basename='plaga')
