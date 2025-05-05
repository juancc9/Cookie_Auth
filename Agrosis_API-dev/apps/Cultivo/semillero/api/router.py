from rest_framework.routers import DefaultRouter
from apps.Cultivo.semillero.api.views import SemilleroViewSet

semilleroRouter = DefaultRouter()

semilleroRouter.register(prefix='semillero', viewset=SemilleroViewSet, basename='semillero')

