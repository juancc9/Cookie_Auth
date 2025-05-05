from rest_framework.routers import DefaultRouter
from apps.Cultivo.ReportePlaga.api.views import ReportePlagaViewSet

reporte_plaga_router = DefaultRouter()
reporte_plaga_router.register(prefix='reportes-plagas', viewset=ReportePlagaViewSet, basename='reportes-plagas')