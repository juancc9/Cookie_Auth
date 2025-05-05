from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

def notificar_asignacion_actividad(actividad, usuarios_ids):
    channel_layer = get_channel_layer()
    
    from apps.Cultivo.actividades.api.serializers import ActividadSerializer
    serializer = ActividadSerializer(actividad)
    actividad_data = serializer.data
    
   
    for user_id in usuarios_ids:
        async_to_sync(channel_layer.group_send)(
            f'user_{user_id}',
            {
                'type': 'send_notification',
                'data': {
                    'type': 'actividad_asignada',
                    'message': 'Se te ha asignado una nueva actividad',
                    'actividad': actividad_data
                }
            }
        )