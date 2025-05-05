import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from apps.Iot.datos_meteorologicos.models import Datos_metereologicos
from apps.Iot.datos_meteorologicos.api.serializers import Datos_metereologicosSerializer
from django.core.exceptions import ObjectDoesNotExist

# Configurar el logger
logger = logging.getLogger(__name__)

class DatosMeteorologicosConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            serializer = Datos_metereologicosSerializer(data=data)
            # Envolver la validación del serializer con database_sync_to_async
            is_valid = await database_sync_to_async(serializer.is_valid)()
            if is_valid:
                validated_data = await database_sync_to_async(lambda: serializer.validated_data)()
                await self.save_data(validated_data)
                await self.send(text_data=json.dumps({"status": "Datos recibidos"}))
                # Limpiar datos para el grupo: eliminar campos vacíos
                cleaned_data = {k: v for k, v in validated_data.items() if v is not None}
                try:
                    await self.channel_layer.group_send(
                        "weather_group",
                        {
                            "type": "weather_data",
                            "data": cleaned_data
                        }
                    )
                except Exception as e:
                    logger.error(f"Error al enviar al grupo: {str(e)}")
                    await self.send(text_data=json.dumps({"warning": f"Error al enviar al grupo: {str(e)}"}))
            else:
                errors = await database_sync_to_async(lambda: serializer.errors)()
                logger.error(f"Error de validación: {errors}")
                await self.send(text_data=json.dumps({"error": errors}))
        except json.JSONDecodeError as e:
            logger.error(f"Datos JSON inválidos: {str(e)}")
            await self.send(text_data=json.dumps({"error": "Datos JSON inválidos"}))
        except Exception as e:
            logger.error(f"Error inesperado en receive: {str(e)}", exc_info=True)
            await self.send(text_data=json.dumps({"error": f"Error inesperado: {str(e)}"}))

    @database_sync_to_async
    def save_data(self, validated_data):
        try:
            Datos_metereologicos.objects.create(**validated_data)
        except ObjectDoesNotExist as e:
            raise ValueError(f"Error de integridad: {str(e)}")
        except Exception as e:
            raise ValueError(f"Error al guardar datos: {str(e)}")

class RealtimeDataConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("weather_group", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("weather_group", self.channel_name)

    async def weather_data(self, event):
        data = event['data']
        await self.send(text_data=json.dumps({
            'type': 'weather_data',
            'data': data
        }))