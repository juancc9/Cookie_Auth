from rest_framework.routers import DefaultRouter
from apps.Cultivo.afecciones.api.views import AfeccionViewSet

afeccionRouter = DefaultRouter()
afeccionRouter.register(prefix='afecciones', viewset=AfeccionViewSet, basename='afecciones')
