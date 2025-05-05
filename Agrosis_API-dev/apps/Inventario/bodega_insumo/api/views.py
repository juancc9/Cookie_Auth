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
from datetime import datetime
import os
from django.conf import settings

from ..models import BodegaInsumo
from .serializers import BodegaInsumoSerializer

class BodegaInsumoViewSet(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = BodegaInsumo.objects.all()
    serializer_class = BodegaInsumoSerializer

    @action(detail=False, methods=['get'])
    def reporte_pdf(self, request):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="reporte_bodega_insumos.pdf"'

        doc = SimpleDocTemplate(response, pagesize=letter)
        elementos = []
        styles = getSampleStyleSheet()

        logo_path = os.path.join(settings.BASE_DIR, "media/logo/def_AGROSIS_LOGOTIC.png")
        if os.path.exists(logo_path):
            logo = Image(logo_path, width=50, height=35)
        else:
            logo = Paragraph("No Logo Disponible", styles["Normal"])

        encabezado_data = [
            [logo, Paragraph("<b>Empresa XYZ</b><br/>Reporte de Bodega de Insumos", styles['Normal']), ""],
            ["", Paragraph(f"Fecha: {datetime.today().strftime('%Y-%m-%d')}", styles['Normal']), "Página 1 de 1"],
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
            "Este documento detalla los insumos almacenados en la bodega, facilitando su control y gestión.",
            styles['Normal'])
        )
        elementos.append(Spacer(1, 15))

        elementos.append(Paragraph("<b>2. Inventario de Insumos</b>", styles['Heading2']))
        elementos.append(Spacer(1, 5))


        bodega_insumos = BodegaInsumo.objects.select_related('bodega', 'insumo').all()
        total_insumos = bodega_insumos.count()
        cantidad_total = sum(insumo.cantidad for insumo in bodega_insumos)

        
        data_insumos = [["ID", "Bodega", "Insumo", "Cantidad"]]
        for insumo in bodega_insumos:
            data_insumos.append([
                insumo.id,
                insumo.bodega.nombre if insumo.bodega else "Sin Bodega",
                insumo.insumo.nombre if insumo.insumo else "Sin Insumo",
                insumo.cantidad
            ])

        tabla_insumos = Table(data_insumos, colWidths=[50, 150, 200, 100])
        tabla_insumos.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.black),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        elementos.append(tabla_insumos)
        elementos.append(Spacer(1, 15))

        
        elementos.append(Paragraph("<b>3. Resumen General</b>", styles['Heading2']))
        resumen_texto = f"""
        Se registraron {total_insumos} tipos de insumos en bodega,
        con un total acumulado de {cantidad_total} unidades.
        """
        elementos.append(Paragraph(resumen_texto, styles['Normal']))

        doc.build(elementos)
        return response
