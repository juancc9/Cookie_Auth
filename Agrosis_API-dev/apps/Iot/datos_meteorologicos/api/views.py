from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.units import inch
from datetime import datetime, timedelta
from apps.Iot.datos_meteorologicos.models import Datos_metereologicos   
from apps.Iot.datos_meteorologicos.api.serializers import Datos_metereologicosSerializer   
from django_filters.rest_framework import DjangoFilterBackend
import os
import logging

# Configurar logging para depuración
logger = logging.getLogger(__name__)

class DatosMeteorologicosViewSet(viewsets.ModelViewSet):
    queryset = Datos_metereologicos.objects.all()
    serializer_class = Datos_metereologicosSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['fk_sensor_id', 'fk_bancal_id', 'fecha_medicion']

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        try:
            logger.info("Ejecutando get_queryset")
            queryset = super().get_queryset()
            logger.info(f"Total de registros en queryset: {queryset.count()}")

            # Filtro por fecha_medicion (en formato YYYY-MM-DD)
            fecha_medicion = self.request.query_params.get('fecha_medicion', None)
            if fecha_medicion:
                try:
                    logger.info(f"Filtrando por fecha_medicion: {fecha_medicion}")
                    fecha = datetime.strptime(fecha_medicion, '%Y-%m-%d')
                    fecha_inicio = fecha
                    fecha_fin = fecha + timedelta(days=1)
                    queryset = queryset.filter(
                        fecha_medicion__gte=fecha_inicio,
                        fecha_medicion__lt=fecha_fin
                    )
                    logger.info(f"Registros después de filtrar por fecha: {queryset.count()}")
                except ValueError as e:
                    logger.error(f"Formato de fecha inválido: {fecha_medicion}, error: {str(e)}")
                    pass

            fk_bancal_id = self.request.query_params.get('fk_bancal_id', None)
            if fk_bancal_id:
                logger.info(f"Filtrando por fk_bancal_id: {fk_bancal_id}")
                queryset = queryset.filter(fk_bancal_id=fk_bancal_id)
                logger.info(f"Registros después de filtrar por bancal: {queryset.count()}")

            return queryset.order_by('-fecha_medicion')
        except Exception as e:
            logger.error(f"Error en get_queryset: {str(e)}")
            raise

    def list(self, request, *args, **kwargs):
        try:
            logger.info("Ejecutando list")
            return super().list(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error en list: {str(e)}")
            raise

    @action(detail=False, methods=['get'])
    def reporte_pdf(self, request):
        try:
            logger.info("Ejecutando reporte_pdf")
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="reporte_datos_meteorologicos.pdf"'

            doc = SimpleDocTemplate(response, pagesize=letter)
            elementos = []
            styles = getSampleStyleSheet()

            logo_path = "media/logo/def_AGROSIS_LOGOTIC.png"
            if not os.path.exists(logo_path):
                logger.error(f"Logo no encontrado en {logo_path}")
                return Response({"error": "Logo no encontrado"}, status=500)

            logo = Image(logo_path, width=50, height=35)
            encabezado_data = [
                [logo, Paragraph("<b>Agrosoft</b><br/>Reporte de Datos Meteorológicos", styles['Normal']), ""],
                ["", Paragraph(f"Fecha: {datetime.today().strftime('%Y-%m-%d')}", styles['Normal']), "Página 1"],
            ]

            tabla_encabezado = Table(encabezado_data, colWidths=[60, 350, 100])
            tabla_encabezado.setStyle(TableStyle([
                ('SPAN', (0, 0), (0, 1)),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            elementos.append(tabla_encabezado)
            elementos.append(Spacer(1, 10))

            elementos.append(Paragraph("<b>1. Objetivo</b>", styles['Heading2']))
            elementos.append(Paragraph(
                "Este documento detalla los datos meteorológicos históricos registrados en el sistema, "
                "facilitando el análisis de las condiciones ambientales para la gestión de cultivos.",
                styles['Normal']
            ))
            elementos.append(Spacer(1, 15))

            elementos.append(Paragraph("<b>2. Registro de Datos Meteorológicos</b>", styles['Heading2']))
            elementos.append(Spacer(1, 5))

            datos = self.get_queryset()
            total_datos = datos.count()
            logger.info(f"Total de datos para el reporte: {total_datos}")

            data_datos = [
                [
                    "ID", "Sensor", "Bancal", "Temp (°C)", "Humedad (%)", "Luz (lux)", 
                    "Lluvia (mm/h)", "V. Viento (m/s)", "D. Viento (°)", 
                    "H. Suelo (%)", "pH Suelo", "Fecha"
                ]
            ]
            for dato in datos:
                try:
                    fecha = dato.fecha_medicion.strftime('%Y-%m-%d %H:%M') if dato.fecha_medicion else "N/A"
                    sensor_nombre = dato.fk_sensor.nombre if dato.fk_sensor and hasattr(dato.fk_sensor, 'nombre') else "N/A"
                    bancal_nombre = dato.fk_bancal.nombre if dato.fk_bancal and hasattr(dato.fk_bancal, 'nombre') else "N/A"
                    data_datos.append([
                        str(dato.id),
                        sensor_nombre,
                        bancal_nombre,
                        str(dato.temperatura) if dato.temperatura is not None else "N/A",
                        str(dato.humedad_ambiente) if dato.humedad_ambiente is not None else "N/A",
                        str(dato.luminosidad) if dato.luminosidad is not None else "N/A",
                        str(dato.lluvia) if dato.lluvia is not None else "N/A",
                        str(dato.velocidad_viento) if dato.velocidad_viento is not None else "N/A",
                        str(dato.direccion_viento) if dato.direccion_viento is not None else "N/A",
                        str(dato.humedad_suelo) if dato.humedad_suelo is not None else "N/A",
                        str(dato.ph_suelo) if dato.ph_suelo is not None else "N/A",
                        fecha
                    ])
                except Exception as e:
                    logger.error(f"Error al procesar dato {dato.id}: {str(e)}")
                    continue

            tabla_datos = Table(data_datos, colWidths=[30, 60, 60, 40, 40, 40, 40, 40, 40, 40, 40, 80])
            tabla_datos.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.black),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 7),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 1), (-1, -1), 'MIDDLE'),
                ('WORDWRAP', (0, 0), (-1, -1), 'CJK'),
            ]))
            elementos.append(tabla_datos)
            elementos.append(Spacer(1, 15))

            elementos.append(Paragraph("<b>3. Resumen General</b>", styles['Heading2']))
            resumen_texto = f"""
            Se registraron {total_datos} mediciones meteorológicas en el sistema.
            """
            elementos.append(Paragraph(resumen_texto, styles['Normal']))

            doc.build(elementos)
            return response
        except Exception as e:
            logger.error(f"Error en reporte_pdf: {str(e)}")
            return Response({"error": str(e)}, status=500)