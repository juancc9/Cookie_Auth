from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.units import inch
from datetime import datetime
from apps.Cultivo.cosechas.models import Cosecha
from apps.Cultivo.cosechas.api.serializers import CosechaSerializer
from apps.Usuarios.usuarios.api.permissions import IsAdminOrRead 
from apps.Usuarios.usuarios.api.permissions import PermisoPorRol
from django.db.models import Sum
from django.db.models.functions import TruncMonth, TruncWeek, ExtractWeekDay

class CosechaViewSet(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrRead, PermisoPorRol] 
    queryset = Cosecha.objects.all()
    serializer_class = CosechaSerializer

    @action(detail=False, methods=['get'])
    def reporte_pdf(self, request):
        
        fecha_inicio = request.GET.get('fecha_inicio')
        fecha_fin = request.GET.get('fecha_fin')

        if not fecha_inicio or not fecha_fin:
            return HttpResponse("Error: Debes proporcionar 'fecha_inicio' y 'fecha_fin'", status=400)

        fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
        fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d")

        cosechas = Cosecha.objects.filter(fecha__range=[fecha_inicio, fecha_fin])
        
        total_cosechas = cosechas.count()
        cantidad_total = sum(c.cantidad for c in cosechas)
        promedio_cosecha = cantidad_total / total_cosechas if total_cosechas > 0 else 0
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="reporte_ingresos_egresos.pdf"'

        doc = SimpleDocTemplate(response, pagesize=letter)
        elementos = []

        styles = getSampleStyleSheet()
        
        logo_path = "media/logo/def_AGROSIS_LOGOTIC.png" 
        logo = Image(logo_path, width=50, height=35)

        encabezado_data = [
            [logo, Paragraph("<b>Centro de gestión y desarrollo sostenible surcolombiano<br/>SENA - YAMBORÓ</b>", styles['Normal']), ""],
            ["", Paragraph("<b>Informe de Cosechas</b>", styles['Heading2']), Paragraph(f"{datetime.today().strftime('%Y-%m-%d')}", styles['Normal'])],
            ["", "", Paragraph("Página 1 de 1", styles['Normal'])],

        ]

        tabla_encabezado = Table(encabezado_data, colWidths=[60, 350, 100])
        tabla_encabezado.setStyle(TableStyle([
            ('SPAN', (0, 0), (0, 2)), 
            ('SPAN', (1, 0), (1, 1)), 
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        elementos.append(tabla_encabezado)



        subtitulo = Paragraph("Informe de cosechas", styles['Heading2'])
        elementos.append(subtitulo)
        elementos.append(Spacer(1, 10))

        objetivo_texto = "Este documento presenta un resumen detallado de las cosechas registradas en el sistema, incluyendo información sobre cultivos, cantidades recolectadas y fechas de cosecha. El objetivo es proporcionar una visión general del rendimiento agrícola para facilitar la toma de decisiones y el análisis de productividad."
        objetivo = Paragraph("<b>1. Objetivo</b><br/>" + objetivo_texto, styles['Normal'])
        elementos.append(objetivo)
        elementos.append(Spacer(1, 15))

        elementos.append(Paragraph("<b>2. Detalle de cosechas</b>", styles['Heading3']))
        elementos.append(Spacer(1, 5))

        data_cosechas = [["Producto", "Cantidad", "Fecha"]]
        for cosecha in cosechas:
            data_cosechas.append([
                cosecha.id_cultivo.nombre,
                cosecha.cantidad,
                cosecha.fecha.strftime("%Y-%m-%d")
            ])

        tabla_ingresos = Table(data_cosechas)
        tabla_ingresos.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.black),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elementos.append(tabla_ingresos)
        elementos.append(Spacer(1, 15))

        elementos.append(Paragraph("<b>3. Resumen General</b>", styles['Heading3']))
        resumen_texto = f"""
        Durante el período del {fecha_inicio} al {fecha_fin}, se registraron {total_cosechas} cosechas. 
        La cantidad total cosechada fue de {cantidad_total} unidades, con un promedio de {promedio_cosecha:.2f} unidades por cosecha.
        """
        elementos.append(Paragraph(resumen_texto, styles['Normal']))

        doc.build(elementos)

        return response
    
    
    @action(detail=False, methods=['get'])
    def datos_graficas(self, request):
        fecha_inicio = request.GET.get('fecha_inicio')
        fecha_fin = request.GET.get('fecha_fin')

        if not fecha_inicio or not fecha_fin:
            return Response({"error": "Debes proporcionar 'fecha_inicio' y 'fecha_fin'"}, status=400)

        cosechas_por_mes = (
            Cosecha.objects
            .filter(fecha__range=[fecha_inicio, fecha_fin])
            .annotate(mes=TruncMonth('fecha'))
            .values('mes')
            .annotate(total=Sum('cantidad'))
            .order_by('mes')
        )

        cosechas_por_cultivo = (
            Cosecha.objects
            .filter(fecha__range=[fecha_inicio, fecha_fin])
            .values('id_cultivo__nombre')
            .annotate(total=Sum('cantidad'))
            .order_by('-total')
        )

        cosechas_por_dia_semana = (
            Cosecha.objects
            .filter(fecha__range=[fecha_inicio, fecha_fin])
            .annotate(dia_semana=ExtractWeekDay('fecha'))
            .values('dia_semana')
            .annotate(total=Sum('cantidad'))
            .order_by('dia_semana')
        )

        dias_nombres = {
            1: 'Lunes',
            2: 'Martes',
            3: 'Miércoles',
            4: 'Jueves',
            5: 'Viernes',
            6: 'Sábado',
            7: 'Domingo'
        }

        data = {
            'por_mes': {
                'meses': [c['mes'].strftime("%Y-%m") for c in cosechas_por_mes],
                'cantidades': [float(c['total']) for c in cosechas_por_mes],
            },
            'por_cultivo': {
                'cultivos': [c['id_cultivo__nombre'] for c in cosechas_por_cultivo],
                'cantidades': [float(c['total']) for c in cosechas_por_cultivo],
            },
            'por_dia_semana': {
                'dias': [dias_nombres.get(c['dia_semana'], 'Desconocido') for c in cosechas_por_dia_semana],
                'cantidades': [float(c['total']) for c in cosechas_por_dia_semana],
            }
        }

        return Response(data)
    

    