from rest_framework.routers import DefaultRouter
from apps.Cultivo.tareas.api.views import TareaViewSet
tareaRouter = DefaultRouter()

tareaRouter.register(prefix='tarea', viewset=TareaViewSet, basename='tarea')
