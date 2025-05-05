from rest_framework.routers import DefaultRouter
from apps.Usuarios.roles.api.views import RolViewSet

RolesRouter = DefaultRouter()
RolesRouter.register(prefix='roles', viewset=RolViewSet, basename='roles')

