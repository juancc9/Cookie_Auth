from rest_framework.routers import DefaultRouter
from apps.Cultivo.bancal.api.views import BancalViewSet

bancalRouter = DefaultRouter()
bancalRouter.register(prefix='Bancal', viewset=BancalViewSet, basename='Bancal')
