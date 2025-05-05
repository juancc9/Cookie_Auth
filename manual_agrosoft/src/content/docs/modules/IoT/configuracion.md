---
title: "Configuración de Sensores"
slug: modules/IoT/configuracion
description: "Ajustes para la configuración de sensores IoT en Arduino IDE para integrarse con Agrosoft."
---

# Configuración de Sensores

La configuración de los sensores IoT no se realiza en la API de Agrosoft, sino en el entorno de desarrollo **Arduino IDE**. Aquí se programan los sensores para recopilar datos (como temperatura y humedad) y enviarlos al servidor de Agrosoft mediante WebSocket o HTTP. A continuación, te explicamos cómo configurar un sensor típico, como el DHT22, usando Arduino IDE.

## Configuración en Arduino IDE

Los sensores deben programarse para conectarse a tu red WiFi y enviar datos al servidor de Agrosoft. Esto se hace escribiendo un programa en Arduino IDE que se carga en una placa compatible (como ESP8266 o ESP32).

### Pasos para Configurar
1. **Instala Arduino IDE:**
   - Descarga e instala Arduino IDE desde [arduino.cc](https://www.arduino.cc/en/software).
   - Conecta tu placa (ej. ESP8266 o ESP32) al ordenador mediante USB.

2. **Instala Librerías Necesarias:**
   - Ve a **Sketch → Include Library → Manage Libraries** en Arduino IDE.
   - Busca e instala:
     - `DHT sensor library` (para sensores DHT como el DHT22).
     - `WebSocketsClient` (para comunicación en tiempo real con Agrosoft).
     - `ESP8266WiFi` o `WiFi` (según tu placa, para conexión a internet).

3. **Escribe el Código:**
   - Crea un nuevo sketch en Arduino IDE. Aquí tienes un ejemplo básico para un sensor DHT22:

```cpp
#include <WiFi.h>
#include <WebSocketsClient.h>
#include <DHT.h>

// Configuración del sensor DHT
#define DHTPIN 4          // Pin donde está conectado el sensor (ej. GPIO 4)
#define DHTTYPE DHT22     // Tipo de sensor (DHT22)

// Configuración de red y servidor
const char* ssid = "TU_RED_WIFI";        // Nombre de tu red WiFi
const char* password = "TU_CONTRASEÑA";  // Contraseña de tu red WiFi
const char* wsServer = "192.168.1.100";  // IP del servidor WebSocket de Agrosoft
const int wsPort = 8080;                 // Puerto del servidor WebSocket
const char* wsPath = "/";                // Ruta del WebSocket

// Objetos
DHT dht(DHTPIN, DHTTYPE);
WebSocketsClient webSocket;

void setup() {
  Serial.begin(115200);
  dht.begin();

  // Conectar a WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConectado a WiFi");

  // Conectar al servidor WebSocket
  webSocket.begin(wsServer, wsPort, wsPath);
}

void loop() {
  webSocket.loop();

  // Leer datos del sensor cada 5 segundos
  delay(5000);
  float temp = dht.readTemperature();
  float hum = dht.readHumidity();

  if (isnan(temp) || isnan(hum)) {
    Serial.println("Error al leer el sensor DHT");
    return;
  }

  // Enviar datos al servidor en formato JSON
  String json = "{\"sensorId\":\"1\",\"temp\":" + String(temp) + ",\"hum\":" + String(hum) + "}";
  webSocket.sendTXT(json);
  Serial.println("Datos enviados: " + json);
}