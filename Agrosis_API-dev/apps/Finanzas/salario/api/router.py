from rest_framework.routers import DefaultRouter
from apps.Finanzas.salario.api.views import SalarioViewSet

salarioRouter = DefaultRouter()
salarioRouter.register(prefix='salario', viewset=SalarioViewSet, basename='salario')