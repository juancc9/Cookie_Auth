# apps/Iot/evapotranspiracion/utils.py
import math
from datetime import datetime, timedelta
from django.db.models import Avg
from apps.Iot.datos_meteorologicos.models import Datos_metereologicos

def calcular_penman_monteith(datos_diarios, latitud, altitud):
    """
    Calcula la evapotranspiración de referencia (ETo) usando el método Penman-Monteith.
    :param datos_diarios: Diccionario con promedios diarios (temperatura, humedad, luminosidad, velocidad_viento).
    :param latitud: Latitud en grados.
    :param altitud: Altitud en metros.
    :return: ETo en mm/día.
    """
    T = datos_diarios['temperatura']  # °C
    RH = datos_diarios['humedad_ambiente']  # %
    u2 = datos_diarios['velocidad_viento']  # m/s
    lux = datos_diarios['luminosidad']  # lux

    Rs = (lux * 0.0079) * (86_400 * 1e-6)  
    P = 101.3 * ((293 - 0.0065 * altitud) / 293) ** 5.26   
    Tmean = T
    delta = 4098 * (0.6108 * math.exp((17.27 * Tmean) / (Tmean + 237.3))) / (Tmean + 237.3) ** 2
    gamma = 0.000665 * P
    es = 0.6108 * math.exp((17.27 * Tmean) / (Tmean + 237.3))
    ea = es * (RH / 100)
    Rn = 0.77 * Rs
    G = 0

    num1 = 0.408 * delta * (Rn - G)
    num2 = gamma * (900 / (Tmean + 273)) * u2 * (es - ea)
    denom = delta + gamma * (1 + 0.34 * u2)
    ETo = (num1 + num2) / denom

    return round(ETo, 2)

def calcular_evapotranspiracion_diaria(bancal_id, fecha, latitud=0, altitud=0):
    """
    Calcula la evapotranspiración para un bancal y fecha específica.
    :param bancal_id: ID del bancal.
    :param fecha: Fecha para el cálculo.
    :param latitud: Latitud del bancal (grados).
    :param altitud: Altitud del bancal (metros).
    :return: Valor de ETo (mm/día).
    """
    fecha_inicio = datetime.combine(fecha, datetime.min.time())
    fecha_fin = fecha_inicio + timedelta(days=1)
    datos = Datos_metereologicos.objects.filter(
        fk_bancal_id=bancal_id,
        fecha_medicion__gte=fecha_inicio,
        fecha_medicion__lt=fecha_fin
    ).aggregate(
        temperatura=Avg('temperatura'),
        humedad_ambiente=Avg('humedad_ambiente'),
        luminosidad=Avg('luminosidad'),
        velocidad_viento=Avg('velocidad_viento')
    )

    if not all(datos.values()):
        return None  

    ETo = calcular_penman_monteith(datos, latitud, altitud)
    return ETo