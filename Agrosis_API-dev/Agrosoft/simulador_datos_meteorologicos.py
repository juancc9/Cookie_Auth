import asyncio
import websockets
import json
import random
from datetime import datetime
import django
import os
import sys

# Añadir el directorio raíz del proyecto al PYTHONPATH
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Agrosoft.settings")
django.setup()

from apps.Iot.sensores.models import Sensor

# Obtener los sensores disponibles
SENSORS = Sensor.objects.all()
SENSOR_TYPES = {sensor.tipo_sensor: sensor.id for sensor in SENSORS}

# Rangos para los datos simulados
DATA_RANGES = {
    "temperatura": (20.0, 30.0),
    "ambient_humidity": (50.0, 70.0),
    "soil_humidity": (40.0, 60.0),
    "luminosidad": (4000.0, 6000.0),
    "lluvia": (0.0, 5.0),
    "velocidad_viento": (0.0, 10.0),
    "direccion_viento": (0, 360),
    "ph_suelo": (6.0, 7.0),
}

async def send_weather_data():
    uri = "ws://127.0.0.1:8000/ws/meteo/"
    while True:
        try:
            async with websockets.connect(uri, ping_interval=20, ping_timeout=30) as websocket:
                print("Conectado a ws/meteo/")
                while True:
                    # Crear datos solo para los tipos de sensores que existen
                    data = {
                        "fk_bancal": 1,  # Asegúrate de que este bancal exista
                        "fecha_medicion": datetime.now().isoformat()
                    }
                    for sensor_type, sensor_id in SENSOR_TYPES.items():
                        data["fk_sensor"] = sensor_id
                        if sensor_type == "direccion_viento":
                            data[sensor_type] = random.randint(*DATA_RANGES[sensor_type])
                        else:
                            data[sensor_type] = round(random.uniform(*DATA_RANGES[sensor_type]), 2)
                        # Enviar un mensaje por cada sensor
                        await websocket.send(json.dumps(data))
                        print(f"Enviado: {data}")
                        try:
                            response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                            print(f"Recibido: {response}")
                        except asyncio.TimeoutError:
                            print("Timeout esperando respuesta, continuando...")
                    await asyncio.sleep(10)
        except (websockets.exceptions.ConnectionClosedError, ConnectionRefusedError) as e:
            print(f"Error de conexión: {e}. Reintentando en 5 segundos...")
            await asyncio.sleep(5)
        except Exception as e:
            print(f"Error inesperado: {e}. Reintentando en 5 segundos...")
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(send_weather_data())