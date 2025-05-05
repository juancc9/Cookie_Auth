import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from apps.Inventario.bodega_herramienta.models import BodegaHerramienta
from channels.layers import get_channel_layer
from django.urls import re_path
import logging
import uuid

logger = logging.getLogger(__name__)

LOW_STOCK_THRESHOLD = 5

class BodegaHerramientaConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.last_update_hash = None

    async def connect(self):
        self.group_name = "bodega_herramienta"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        await self.send_initial_state()

    async def disconnect(self, close_code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data.get("action") == "sync":
            await self.send_initial_state()
        elif data.get("action") == "use_herramienta":
            await self.handle_herramienta_usage(data)

    @database_sync_to_async
    def get_all_herramientas(self):
        return [
            {
                "id": h.id,
                "bodega": h.bodega.nombre if h.bodega else "Desconocido",
                "herramienta": h.herramienta.nombre if h.herramienta else "Desconocido",
                "cantidad": h.cantidad or 0
            }
            for h in BodegaHerramienta.objects.all()
        ]

    @database_sync_to_async
    def update_herramienta_quantity(self, herramienta_id, cantidad_usada):
        try:
            herramienta = BodegaHerramienta.objects.get(herramienta_id=herramienta_id)
            if herramienta.cantidad >= cantidad_usada:
                herramienta.cantidad -= cantidad_usada
                herramienta.save()
                return {
                    "id": herramienta.id,
                    "bodega": herramienta.bodega.nombre if herramienta.bodega else "Desconocido",
                    "herramienta": herramienta.herramienta.nombre if herramienta.herramienta else "Desconocido",
                    "cantidad": herramienta.cantidad,
                    "cantidad_usada": cantidad_usada
                }
            else:
                logger.error(f"No hay suficiente cantidad en {herramienta.herramienta.nombre} para usar {cantidad_usada}")
                return None
        except BodegaHerramienta.DoesNotExist:
            logger.error(f"Herramienta con ID {herramienta_id} no encontrada en BodegaHerramienta")
            return None

    async def send_initial_state(self):
        herramientas = await self.get_all_herramientas()
        message = {
            "type": "initial_state",
            "message": herramientas,
            "timestamp": str(uuid.uuid4())
        }
        message_json = json.dumps(message)
        await self.send_update({"message": message, "message_json": message_json})

    async def handle_herramienta_usage(self, data):
        herramienta_id = data.get("herramienta_id")
        cantidad_usada = data.get("cantidad_usada", 0)
        if not herramienta_id or not isinstance(cantidad_usada, (int, float)) or cantidad_usada <= 0:
            logger.error("Datos inválidos para uso de herramienta")
            return

        updated_herramienta = await self.update_herramienta_quantity(herramienta_id, cantidad_usada)
        if updated_herramienta:
            if updated_herramienta["cantidad"] <= LOW_STOCK_THRESHOLD:
                message = {
                    "message_id": f"low_stock-{updated_herramienta['id']}-{uuid.uuid4()}",
                    "id": updated_herramienta["id"],
                    "bodega": updated_herramienta["bodega"],
                    "herramienta": updated_herramienta["herramienta"],
                    "cantidad": updated_herramienta["cantidad"],
                    "type": "low_stock",
                    "timestamp": str(uuid.uuid4())
                }
                message_json = json.dumps(message)
                await self.channel_layer.group_send(
                    "bodega_herramienta",
                    {
                        "type": "send_update",
                        "message": message,
                        "message_json": message_json
                    }
                )

    async def send_update(self, event):
        message_json = event.get("message_json", json.dumps(event["message"]))
        current_hash = hash(message_json)
        if current_hash == self.last_update_hash:
            logger.info("Mensaje duplicado ignorado en send_update")
            return
        self.last_update_hash = current_hash
        await self.send(text_data=json.dumps(event["message"]))

sent_messages = set()

@receiver(post_save, sender=BodegaHerramienta)
def herramienta_saved(sender, instance, created, **kwargs):
    channel_layer = get_channel_layer()
    action = "create" if created else "update"
    logger.info(f"post_save disparado: id={instance.id}, action={action}")

    message_id = f"{action}-{instance.id}-{uuid.uuid4()}"
    message_key = f"{action}-{instance.id}"
    if message_key in sent_messages:
        logger.warning(f"Mensaje duplicado detectado: {message_key}")
        return
    sent_messages.add(message_key)

    try:
        bodega_name = instance.bodega.nombre if instance.bodega else "Desconocido"
    except Exception as e:
        logger.error(f"Error al obtener bodega.nombre: {e}")
        bodega_name = "Desconocido"

    try:
        herramienta_name = instance.herramienta.nombre if instance.herramienta else "Desconocido"
    except Exception as e:
        logger.error(f"Error al obtener herramienta.nombre: {e}")
        herramienta_name = "Desconocido"

    def send_update():
        message = {
            "message_id": message_id,
            "id": instance.id,
            "bodega": bodega_name,
            "herramienta": herramienta_name,
            "cantidad": instance.cantidad or 0,
            "type": action,
            "timestamp": str(uuid.uuid4())
        }
        message_json = json.dumps(message)
        async_to_sync(channel_layer.group_send)(
            "bodega_herramienta",
            {
                "type": "send_update",
                "message": message,
                "message_json": message_json
            }
        )

    send_update()

@receiver(post_delete, sender=BodegaHerramienta)
def herramienta_deleted(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    logger.info(f"post_delete disparado: id={instance.id}")

    message_id = f"delete-{instance.id}-{uuid.uuid4()}"
    message_key = f"delete-{instance.id}"
    if message_key in sent_messages:
        logger.warning(f"Mensaje duplicado detectado: {message_key}")
        return
    sent_messages.add(message_key)

    def send_update():
        message = {
            "message_id": message_id,
            "id": instance.id,
            "type": "delete",
            "timestamp": str(uuid.uuid4())
        }
        message_json = json.dumps(message)
        async_to_sync(channel_layer.group_send)(
            "bodega_herramienta",
            {
                "type": "send_update",
                "message": message,
                "message_json": message_json
            }
        )

    send_update()

websocket_urlpatterns = [
    re_path(r'ws/inventario/bodega_herramienta/$', BodegaHerramientaConsumer.as_asgi())
]