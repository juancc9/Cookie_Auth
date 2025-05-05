from django.urls import re_path
from .consumers import BodegaHerramientaConsumer

websocket_urlpatterns = [
    re_path(r'ws/inventario/bodega_herramienta/$', BodegaHerramientaConsumer.as_asgi()),
]
