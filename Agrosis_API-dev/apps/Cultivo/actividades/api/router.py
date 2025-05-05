from rest_framework.routers import DefaultRouter
from apps.Cultivo.actividades.api.views import ActividadViewSet
actividadRouter = DefaultRouter()

actividadRouter.register(prefix='actividades', viewset=ActividadViewSet, basename='actividades')
