from django.urls import re_path
from apps.Cultivo.actividades.api.consumers import ActividadNotificacionConsumer

websocket_urlpatterns = [
re_path(r'ws/actividades/notificaciones/(?P<user_id>\d+)/$', ActividadNotificacionConsumer.as_asgi()),
]