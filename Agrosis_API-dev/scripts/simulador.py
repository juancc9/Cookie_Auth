import websockets
import asyncio
import json

async def listen():
    uri = "ws://localhost:8000/ws/meteo/"
    
    async with websockets.connect(uri) as websocket:
        while True:
            response = await websocket.recv()
            data = json.loads(response)
            print(f"📡 Sensor: {data['tipo_sensor']} - Valor: {data['valor']} - {data.get('alerta', '')}")

asyncio.run(listen())
