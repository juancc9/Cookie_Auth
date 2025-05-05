---
title: "Datos Meteorológicos"
slug: modules/IoT/datos-meteorologicos
description: "Registro y visualización de datos meteorológicos en Agrosoft."
---

# Datos Meteorológicos

Los datos meteorológicos, como temperatura y humedad, son recopilados por los sensores **IoT** y se integran en **Agrosoft** para monitorear las condiciones de los cultivos en tiempo real.

## Registro de Datos
- Los sensores envían datos a través de **WebSocket** para actualizaciones en tiempo real.
- Los datos históricos se almacenan mediante peticiones **HTTP** y están disponibles en la sección **IoT → Datos Meteorológicos**.
- Cada registro incluye:
  - **ID del Sensor:** Identificador del sensor que generó el dato.
  - **Temperatura:** Valor en grados Celsius.
  - **Humedad:** Valor en porcentaje.
  - **Fecha y Hora:** Marca temporal de la medición.

## Visualización
- Accede a **IoT → Sensores y Datos Historicos** para ver gráficos y tablas.
- Los datos se presentan en:
  - **Gráficos en tiempo real:** Actualizados vía **WebSocket**.
  - **Historial:** Filtrable por fecha y sensor.