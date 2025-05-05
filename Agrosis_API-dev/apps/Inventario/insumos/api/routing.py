from django.urls import re_path
from .consumers import InsumoConsumer

websocket_urlpatterns = [
    re_path(r'^ws/insumo/(?P<user_id>\d+)/$', InsumoConsumer.as_asgi()),
    re_path(r'^ws/insumo/admin/$', InsumoConsumer.as_asgi()),
]