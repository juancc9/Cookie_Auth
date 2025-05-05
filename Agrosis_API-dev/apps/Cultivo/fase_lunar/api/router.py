from rest_framework.routers import DefaultRouter
from apps.Cultivo.fase_lunar.api.views import FaseLunarViewSet

faseLunarRouter = DefaultRouter()
faseLunarRouter.register(prefix='faselunar', viewset=FaseLunarViewSet, basename='faselunar')

