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
from datetime import datetime, timedelta
from django.utils import timezone
from apps.Finanzas.venta.models import Venta
from apps.Finanzas.venta.api.serializers import VentaSerializer
from apps.Usuarios.usuarios.api.permissions import IsAdminOrRead 
from django.db.models import Sum
from django.db.models.functions import TruncMonth, ExtractWeekDay
class VentaViewSet(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrRead]
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer

    @action(detail=False, methods=['get'])
    def reporte_pdf(self, request):
        fecha_inicio = request.GET.get('fecha_inicio')
        fecha_fin = request.GET.get('fecha_fin')

        if not fecha_inicio or not fecha_fin:
            return HttpResponse("Error: Debes proporcionar 'fecha_inicio' y 'fecha_fin'", status=400)

        fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
        fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d")

        ventas = Venta.objects.filter(fecha__range=[fecha_inicio, fecha_fin])
        
        total_ventas = ventas.count()
        ingresos_totales = sum(v.total for v in ventas)
        promedio_venta = ingresos_totales / total_ventas if total_ventas > 0 else 0

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="reporte_ventas.pdf"'

        doc = SimpleDocTemplate(response, pagesize=letter)
        elementos = []

        styles = getSampleStyleSheet()
        
        logo_path = "media/logo/def_AGROSIS_LOGOTIC.png" 
        logo = Image(logo_path, width=50, height=35)

        encabezado_data = [
            [logo, Paragraph("<b>Centro de gestión y desarrollo sostenible surcolombiano<br/>SENA - YAMBORÓ</b>", styles['Normal']), ""],
            ["", Paragraph("<b>Informe de Ventas</b>", styles['Heading2']), Paragraph(f"{datetime.today().strftime('%Y-%m-%d')}", styles['Normal'])],
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

        subtitulo = Paragraph("Informe de ventas", styles['Heading2'])
        elementos.append(subtitulo)
        elementos.append(Spacer(1, 10))

        objetivo_texto = "Este documento presenta un resumen detallado de las ventas registradas en el sistema, incluyendo información sobre productos, cantidades vendidas, montos totales y fechas de venta. El objetivo es proporcionar una visión general del desempeño comercial para facilitar el análisis financiero y la toma de decisiones."
        objetivo = Paragraph("<b>1. Objetivo</b><br/>" + objetivo_texto, styles['Normal'])
        elementos.append(objetivo)
        elementos.append(Spacer(1, 15))

        elementos.append(Paragraph("<b>2. Detalle de ventas</b>", styles['Heading3']))
        elementos.append(Spacer(1, 5))

        data_ventas = [["Producto", "Cantidad", "Precio Unitario", "Total", "Fecha"]]
        for venta in ventas:
            data_ventas.append([
                venta.producto.Producto.id_cultivo.nombre,
                venta.cantidad,
                f"${venta.producto.precio}",
                f"${venta.total}",
                venta.fecha.strftime("%Y-%m-%d")
            ])

        tabla_ventas = Table(data_ventas, colWidths=[150, 60, 80, 80, 80])
        tabla_ventas.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.black),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elementos.append(tabla_ventas)
        elementos.append(Spacer(1, 15))

        elementos.append(Paragraph("<b>3. Resumen General</b>", styles['Heading3']))
        resumen_texto = f"""
        Durante el período del {fecha_inicio.strftime('%Y-%m-%d')} al {fecha_fin.strftime('%Y-%m-%d')}, se registraron {total_ventas} ventas. 
        Los ingresos totales fueron de ${ingresos_totales:.2f}, con un promedio de ${promedio_venta:.2f} por venta.
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

        try:
            fecha_inicio_dt = timezone.make_aware(datetime.strptime(fecha_inicio, '%Y-%m-%d'))
            fecha_fin_dt = timezone.make_aware(datetime.strptime(fecha_fin, '%Y-%m-%d') + timedelta(days=1))
        except ValueError:
            return Response({"error": "Formato de fecha inválido. Use YYYY-MM-DD"}, status=400)

        ventas = Venta.objects.filter(fecha__range=[fecha_inicio_dt, fecha_fin_dt])

        ventas_por_mes = (
            ventas
            .annotate(mes=TruncMonth('fecha'))
            .values('mes')
            .annotate(total=Sum('total'), cantidad=Sum('cantidad'))
            .order_by('mes')
        )

        ventas_por_producto = (
            ventas
            .values('producto__Producto')
            .annotate(total=Sum('total'), cantidad=Sum('cantidad'))
            .order_by('-total')
        )

        ventas_por_dia_semana = (
            ventas
            .annotate(dia_semana=ExtractWeekDay('fecha'))
            .values('dia_semana')
            .annotate(total=Sum('total'), cantidad=Sum('cantidad'))
            .order_by('dia_semana')
        )

        dias_nombres = {
            1: 'Domingo',
            2: 'Lunes',
            3: 'Martes',
            4: 'Miércoles',
            5: 'Jueves',
            6: 'Viernes',
            7: 'Sábado'
        }

        dias_completos = []
        for dia_num in range(1, 8):
            dia_data = next((item for item in ventas_por_dia_semana if item['dia_semana'] == dia_num), None)
            dias_completos.append({
                'dia_semana': dia_num,
                'total': dia_data['total'] if dia_data else 0,
                'cantidad': dia_data['cantidad'] if dia_data else 0
            })

        resumen = {
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'total_ingresos': ventas.aggregate(Sum('total'))['total__sum'] or 0,
            'total_cantidad': ventas.aggregate(Sum('cantidad'))['cantidad__sum'] or 0,
            'total_transacciones': ventas.count()
        }

        data = {
            'resumen': resumen,
            'por_mes': {
                'meses': [v['mes'].strftime("%Y-%m") for v in ventas_por_mes],
                'ingresos': [float(v['total']) for v in ventas_por_mes],
                'cantidades': [float(v['cantidad']) for v in ventas_por_mes],
            },
            'por_producto': {
                'productos': [v['producto__Producto'] for v in ventas_por_producto],
                'ingresos': [float(v['total']) for v in ventas_por_producto],
                'cantidades': [float(v['cantidad']) for v in ventas_por_producto],
            },
            'por_dia_semana': {
                'dias': [dias_nombres[dia['dia_semana']] for dia in dias_completos],
                'ingresos': [float(dia['total']) for dia in dias_completos],
                'cantidades': [float(dia['cantidad']) for dia in dias_completos],
            }
        }

        return Response(data)