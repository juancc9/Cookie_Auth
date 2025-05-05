from rest_framework.routers import DefaultRouter
from apps.Cultivo.especies.api.views import EspecieViewSet

especiesRouter = DefaultRouter()
especiesRouter.register(prefix='especies', viewset=EspecieViewSet, basename='especies')
