from django.db.models.signals import post_migrate
from django.dispatch import receiver
from apps.Iot.sensores.models import TipoSensor

@receiver(post_migrate)
def create_tipo_sensores(sender, **kwargs):
    tipos = [
        {"nombre": "temperatura", "unidad_medida": "°C", "medida_minima": -40, "medida_maxima": 125, "descripcion": "Mide la temperatura ambiente"},
        {"nombre": "humedad_ambiente", "unidad_medida": "%", "medida_minima": 0, "medida_maxima": 100, "descripcion": "Mide la humedad del aire"},
        {"nombre": "luminosidad", "unidad_medida": "lux", "medida_minima": 0, "medida_maxima": 100000, "descripcion": "Mide la intensidad de la luz"},
        {"nombre": "lluvia", "unidad_medida": "mm/h", "medida_minima": 0, "medida_maxima": 500, "descripcion": "Mide la precipitación"},
        {"nombre": "velocidad_viento", "unidad_medida": "m/s", "medida_minima": 0, "medida_maxima": 100, "descripcion": "Mide la velocidad del viento"},
        {"nombre": "direccion_viento", "unidad_medida": "°", "medida_minima": 0, "medida_maxima": 360, "descripcion": "Mide la dirección del viento"},
        {"nombre": "humedad_suelo", "unidad_medida": "%", "medida_minima": 0, "medida_maxima": 100, "descripcion": "Mide la humedad del suelo"},
        {"nombre": "ph_suelo", "unidad_medida": "", "medida_minima": 0, "medida_maxima": 14, "descripcion": "Mide el pH del suelo"},
    ]
    for tipo in tipos:
        TipoSensor.objects.get_or_create(
            nombre=tipo["nombre"],
            defaults={
                "unidad_medida": tipo["unidad_medida"],
                "medida_minima": tipo["medida_minima"],
                "medida_maxima": tipo["medida_maxima"],
                "descripcion": tipo["descripcion"],
            }
        )