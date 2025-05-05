from rest_framework.routers import DefaultRouter
from apps.Cultivo.programacion.api.views import ProgramacionViewSet

programacionRouter = DefaultRouter()
programacionRouter.register(prefix='programacion', viewset=ProgramacionViewSet, basename='programacion')

