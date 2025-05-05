from django.urls import re_path
from .consumers import BodegaInsumoConsumer

websocket_urlpatterns = [
    re_path(r'ws/inventario/bodega_insumo/$', BodegaInsumoConsumer.as_asgi()),
]