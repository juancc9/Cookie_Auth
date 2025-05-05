from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from apps.Finanzas.pagos.models import Pago
from rest_framework.permissions import IsAuthenticated
from apps.Finanzas.pagos.api.serializers import PagoSerializer, CalculoPagoSerializer, PagoCreateSerializer
from django.db.models import Sum
from django.db.models.functions import TruncMonth, ExtractWeekDay
from datetime import datetime, timedelta

from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from django.http import HttpResponse
from apps.Usuarios.usuarios.api.permissions import PermisoPorRol


class PagoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, PermisoPorRol]
    queryset = Pago.objects.all().prefetch_related('actividades__usuarios', 'salario')

    
    serializer_class = PagoSerializer

    @action(detail=False, methods=['get'], url_path='reporte_pdf')
    def reporte_pdf(self, request):
        fecha_inicio_str = request.GET.get('fecha_inicio')
        fecha_fin_str = request.GET.get('fecha_fin')

        if not fecha_inicio_str or not fecha_fin_str:
            return HttpResponse("Debes proporcionar 'fecha_inicio' y 'fecha_fin'", status=400)

        fecha_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%d")
        fecha_fin = datetime.strptime(fecha_fin_str, "%Y-%m-%d") + timedelta(days=1)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="reporte_pagos_por_mes.pdf"'

        doc = SimpleDocTemplate(response, pagesize=letter)
        elementos = []
        styles = getSampleStyleSheet()

        logo_path = "media/logo/def_AGROSIS_LOGOTIC.png"
        logo = Image(logo_path, width=50, height=35)

        encabezado = Table([
            [logo, Paragraph("<b>Centro de gestión y desarrollo sostenible surcolombiano<br/>SENA - YAMBORÓ</b>", styles['Normal']), ""],
            ["", Paragraph("<b>Informe de Pagos por Usuario</b>", styles['Heading2']), Paragraph(f"{datetime.today().strftime('%Y-%m-%d')}", styles['Normal'])],
            ["", "", Paragraph("Página 1 de 1", styles['Normal'])]
        ], colWidths=[60, 350, 100])
        encabezado.setStyle(TableStyle([
            ('SPAN', (0, 0), (0, 2)),
            ('SPAN', (1, 0), (1, 1)),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elementos.append(encabezado)
        elementos.append(Spacer(1, 15))

        pagos_por_mes = (
            Pago.objects
            .filter(fecha_calculo__range=[fecha_inicio, fecha_fin])
            .annotate(mes=TruncMonth('fecha_calculo'))
            .values('mes')
            .distinct()
            .order_by('mes')
        )

        for mes_info in pagos_por_mes:
            mes = mes_info['mes']
            elementos.append(Paragraph(f"<b>Mes: {mes.strftime('%B %Y')}</b>", styles['Heading3']))
            elementos.append(Spacer(1, 5))

            pagos_mes = (
                Pago.objects
                .filter(fecha_calculo__year=mes.year, fecha_calculo__month=mes.month)
                .values('actividades__usuarios__nombre')
                .annotate(total_pago=Sum('total_pago'))
                .order_by('-total_pago')
            )

            if pagos_mes:
                data = [["Usuario", "Total Pagado"]]
                for p in pagos_mes:
                    data.append([p['actividades__usuarios__nombre'], f"${p['total_pago']:.2f}"])
                tabla = Table(data, colWidths=[300, 200])
                tabla.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.black),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ]))
                elementos.append(tabla)
            else:
                elementos.append(Paragraph("No hay pagos registrados en este mes.", styles['Normal']))
            elementos.append(Spacer(1, 20))

        doc.build(elementos)
        return response


    def get_serializer_class(self):
        if self.action == 'create':
            return PagoCreateSerializer
        if self.action == 'calcular_pago':
            return CalculoPagoSerializer
        return PagoSerializer

    def create(self, request, *args, **kwargs):
        return Response(
            {"error": "Use el endpoint /calcular_pago/ para crear pagos"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    @action(detail=False, methods=['post'])
    def calcular_pago(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                pago = serializer.save()
                return Response(
                    PagoSerializer(pago, context={'request': request}).data,
                    status=status.HTTP_201_CREATED
                )
            except ValidationError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='datos_graficas')
    def datos_graficas(self, request):
        fecha_inicio_str = request.GET.get('fecha_inicio')
        fecha_fin_str = request.GET.get('fecha_fin')

        if not fecha_inicio_str or not fecha_fin_str:
            return Response({"error": "Debes proporcionar 'fecha_inicio' y 'fecha_fin'"}, status=400)

        # Parseamos las fechas y extendemos el rango para cubrir todo el día final
        fecha_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%d")
        fecha_fin = datetime.strptime(fecha_fin_str, "%Y-%m-%d") + timedelta(days=1)

        pagos_por_mes = (
            Pago.objects
            .filter(fecha_calculo__range=[fecha_inicio, fecha_fin])
            .annotate(mes=TruncMonth('fecha_calculo'))
            .values('mes')
            .annotate(total_pago=Sum('total_pago'))
            .order_by('mes')
        )

        pagos_por_usuario = (
            Pago.objects
            .filter(fecha_calculo__range=[fecha_inicio, fecha_fin])
            .values('actividades__usuarios__nombre')  # nombre del usuario relacionado
            .annotate(total_pago=Sum('total_pago'))
            .order_by('-total_pago')
        )

        pagos_por_dia_semana = (
            Pago.objects
            .filter(fecha_calculo__range=[fecha_inicio, fecha_fin])
            .annotate(dia_semana=ExtractWeekDay('fecha_calculo'))
            .values('dia_semana')
            .annotate(total_pago=Sum('total_pago'))
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

        usuarios_top_por_mes = []
        for entry in pagos_por_mes:
            mes_actual = entry['mes']
            pagos_mes = (
                Pago.objects
                .filter(fecha_calculo__month=mes_actual.month, fecha_calculo__year=mes_actual.year)
                .values('actividades__usuarios__nombre')
                .annotate(total_usuario=Sum('total_pago'))
                .order_by('-total_usuario')
            )
            if pagos_mes:
                usuarios_top_por_mes.append(pagos_mes[0]['actividades__usuarios__nombre'])
            else:
                usuarios_top_por_mes.append("Sin datos")

        data = {
            'por_mes': {
                'meses': [p['mes'].strftime("%Y-%m") for p in pagos_por_mes],
                'total_pago': [float(p['total_pago']) for p in pagos_por_mes],
                'usuario_top': usuarios_top_por_mes,
            },
            'por_usuario': {
                'usuarios': [p['actividades__usuarios__nombre'] for p in pagos_por_usuario],
                'total_pago': [float(p['total_pago']) for p in pagos_por_usuario],
            },
            'por_dia_semana': {
                'dias': [dias_nombres.get(p['dia_semana'], 'Desconocido') for p in pagos_por_dia_semana],
                'total_pago': [float(p['total_pago']) for p in pagos_por_dia_semana],
            }
        }

        return Response(data)
