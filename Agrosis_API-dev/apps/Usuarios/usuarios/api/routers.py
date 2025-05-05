from rest_framework.routers import DefaultRouter
from apps.Usuarios.usuarios.api.views import UsuariosViewSet

UsuariosRouter = DefaultRouter()
UsuariosRouter.register(prefix='usuarios', viewset=UsuariosViewSet, basename='usuarios')