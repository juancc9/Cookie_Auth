import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from ..models import Insumo
from django.utils import timezone
from datetime import timedelta
import hashlib

User = get_user_model()

class InsumoConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sent_notifications = set()  # Conjunto para rastrear notificaciones enviadas
        self.check_task = None

    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs'].get('user_id')
        print(f"Conectando WebSocket para user_id: {self.user_id}")
        
        if self.user_id == 'admin':
            self.group_name = "insumo_admin_group"
        else:
            try:
                self.user_id = int(self.user_id)
                if not await self.get_user(self.user_id):
                    print(f"Usuario {self.user_id} no encontrado, cerrando conexión")
                    await self.close(code=4001)
                    return
                
                self.group_name = f"insumo_user_{self.user_id}"
                await self.channel_layer.group_send(
                    self.group_name,
                    {
                        "type": "force_disconnect",
                        "message": "Nueva conexión establecida"
                    }
                )
            except (ValueError, TypeError) as e:
                print(f"Error en user_id: {e}, cerrando conexión")
                await self.close(code=4000)
                return

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        print(f"Conexión aceptada para {self.group_name}")
        self.check_task = asyncio.create_task(self.periodic_check())

    async def force_disconnect(self, event):
        print(f"Desconexión forzada: {event['message']}")
        await self.close(code=4002)

    async def disconnect(self, close_code):
        print(f"WebSocket desconectado con código: {close_code}")
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)
        if self.check_task:
            self.check_task.cancel()

    async def send_notification(self, event):
        current_hash = event['hash']
        if current_hash in self.sent_notifications:
            print(f"Notificación duplicada ignorada: {current_hash}")
            return
            
        self.sent_notifications.add(current_hash)
        message_data = {
            'message': event['message'],
            'notification_type': event.get('notification_type', 'info'),
            'timestamp': event.get('timestamp'),
            'insumo_id': event.get('insumo_id'),
            'hash': current_hash
        }
        print(f"Enviando notificación al cliente: {message_data}")
        await self.send(text_data=json.dumps(message_data))

    @database_sync_to_async
    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

    @database_sync_to_async
    def check_insumos(self):
        insumos = Insumo.objects.filter(activo=True)
        notificaciones = []
        
        today = timezone.now().date()
        umbral_cantidad = 10 
        umbral_dias = 7       
        
        for insumo in insumos:
            timestamp = str(int(timezone.now().timestamp() * 1000))
            # Hash basado solo en insumo_id y tipo de notificación
            if insumo.cantidad <= umbral_cantidad:
                insumo_hash = hashlib.md5(f"{insumo.id}low_stock".encode()).hexdigest()
                notif = {
                    "insumo_id": insumo.id,
                    "message": f"El insumo {insumo.nombre} está bajo en stock: {insumo.cantidad} {insumo.unidad_medida} restantes.",
                    "notification_type": "warning",
                    "timestamp": timestamp,
                    "hash": insumo_hash
                }
                print(f"Notificación generada: {notif}")
                notificaciones.append(notif)
            if insumo.fecha_caducidad and (insumo.fecha_caducidad - today).days <= umbral_dias:
                insumo_hash = hashlib.md5(f"{insumo.id}expiring".encode()).hexdigest()
                notif = {
                    "insumo_id": insumo.id,
                    "message": f"El insumo {insumo.nombre} está próximo a vencer: {insumo.fecha_caducidad}.",
                    "notification_type": "alert",
                    "timestamp": timestamp,
                    "hash": insumo_hash
                }
                print(f"Notificación generada: {notif}")
                notificaciones.append(notif)
        
        return notificaciones

    async def periodic_check(self):
        while True:
            try:
                print(f"Verificando insumos para {self.group_name}")
                notificaciones = await self.check_insumos()
                for notif in notificaciones:
                    await self.channel_layer.group_send(
                        self.group_name,
                        {
                            "type": "send_notification",
                            "message": notif["message"],
                            "notification_type": notif["notification_type"],
                            "timestamp": notif["timestamp"],
                            "insumo_id": notif["insumo_id"],
                            "hash": notif["hash"]
                        }
                    )
                await asyncio.sleep(300) 
            except asyncio.CancelledError:
                print("Tarea periódica cancelada")
                break
            except Exception as e:
                print(f"Error en periodic_check: {e}")
                await asyncio.sleep(300)