from django.urls import re_path
from apps.Iot.datos_meteorologicos.api.consumer import DatosMeteorologicosConsumer, RealtimeDataConsumer
from apps.Cultivo.actividades.api.routing import websocket_urlpatterns as actividad_ws
from apps.Inventario.bodega_herramienta.api.routing import websocket_urlpatterns as herramienta_ws
from apps.Inventario.bodega_insumo.api.routing import websocket_urlpatterns as bodega_insumo_ws
from apps.Inventario.insumos.api.routing import websocket_urlpatterns as insumo_ws

meteo_ws = [
    re_path(r"ws/meteo/$", DatosMeteorologicosConsumer.as_asgi()),
    re_path(r"ws/realtime/$", RealtimeDataConsumer.as_asgi()),
]

websocket_urlpatterns = meteo_ws + actividad_ws + insumo_ws + herramienta_ws + bodega_insumo_ws