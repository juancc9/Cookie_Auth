from rest_framework.routers import DefaultRouter
from apps.Cultivo.lotes.api.views import LoteViewSet

lotesRouter = DefaultRouter()
lotesRouter.register(prefix='lote', viewset=LoteViewSet, basename='lote')

