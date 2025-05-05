import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from apps.Inventario.bodega_insumo.models import BodegaInsumo
from channels.layers import get_channel_layer
import logging
import uuid

logger = logging.getLogger(__name__)

LOW_STOCK_THRESHOLD = 5

class BodegaInsumoConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.last_update_hash = None

    async def connect(self):
        self.group_name = "bodega_insumo"
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
        elif data.get("action") == "use_insumo":
            await self.handle_insumo_usage(data)

    @database_sync_to_async
    def get_all_insumos(self):
        return [
            {
                "id": i.id,
                "bodega": i.bodega.nombre if i.bodega else "Desconocido",
                "insumo": i.insumo.nombre if i.insumo else "Desconocido",
                "cantidad": i.cantidad or 0
            }
            for i in BodegaInsumo.objects.all()
        ]

    @database_sync_to_async
    def update_insumo_quantity(self, insumo_id, cantidad_usada):
        try:
            insumo = BodegaInsumo.objects.get(insumo_id=insumo_id) 
            if insumo.cantidad >= cantidad_usada:
                insumo.cantidad -= cantidad_usada
                insumo.save()
                return {
                    "id": insumo.id,
                    "bodega": insumo.bodega.nombre if insumo.bodega else "Desconocido",
                    "insumo": insumo.insumo.nombre if insumo.insumo else "Desconocido",
                    "cantidad": insumo.cantidad,
                    "cantidad_usada": cantidad_usada
                }
            else:
                logger.error(f"No hay suficiente cantidad en {insumo.insumo.nombre} para usar {cantidad_usada}")
                return None
        except BodegaInsumo.DoesNotExist:
            logger.error(f"Insumo con ID {insumo_id} no encontrado en BodegaInsumo")
            return None

    async def send_initial_state(self):
        insumos = await self.get_all_insumos()
        message = {
            "type": "initial_state",
            "message": insumos,
            "timestamp": str(uuid.uuid4())
        }
        message_json = json.dumps(message)
        await self.send_update({"message": message, "message_json": message_json})

    async def handle_insumo_usage(self, data):
        insumo_id = data.get("insumo_id")
        cantidad_usada = data.get("cantidad_usada", 0)
        if not insumo_id or not isinstance(cantidad_usada, (int, float)) or cantidad_usada <= 0:
            logger.error("Datos inválidos para uso de insumo")
            return

        updated_insumo = await self.update_insumo_quantity(insumo_id, cantidad_usada)
        if updated_insumo:
            if updated_insumo["cantidad"] <= LOW_STOCK_THRESHOLD:
                message = {
                    "message_id": f"low_stock-{updated_insumo['id']}-{uuid.uuid4()}",
                    "id": updated_insumo["id"],
                    "bodega": updated_insumo["bodega"],
                    "insumo": updated_insumo["insumo"],
                    "cantidad": updated_insumo["cantidad"],
                    "type": "low_stock",
                    "timestamp": str(uuid.uuid4())
                }
                message_json = json.dumps(message)
                await self.channel_layer.group_send(
                    "bodega_insumo",
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

@receiver(post_save, sender=BodegaInsumo)
def insumo_saved(sender, instance, created, **kwargs):
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
        insumo_name = instance.insumo.nombre if instance.insumo else "Desconocido"
    except Exception as e:
        logger.error(f"Error al obtener insumo.nombre: {e}")
        insumo_name = "Desconocido"

    def send_update():
        message = {
            "message_id": message_id,
            "id": instance.id,
            "bodega": bodega_name,
            "insumo": insumo_name,
            "cantidad": instance.cantidad or 0,
            "type": action,
            "timestamp": str(uuid.uuid4())
        }
        message_json = json.dumps(message)
        async_to_sync(channel_layer.group_send)(
            "bodega_insumo",
            {
                "type": "send_update",
                "message": message,
                "message_json": message_json
            }
        )

    send_update()

@receiver(post_delete, sender=BodegaInsumo)
def insumo_deleted(sender, instance, **kwargs):
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
            "bodega_insumo",
            {
                "type": "send_update",
                "message": message,
                "message_json": message_json
            }
        )

    send_update()