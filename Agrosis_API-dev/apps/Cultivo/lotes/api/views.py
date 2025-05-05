from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from apps.Cultivo.lotes.models import Lote
from apps.Cultivo.lotes.api.serializers import LoteSerializer
from apps.Usuarios.usuarios.api.permissions import IsAdminOrRead
from apps.Usuarios.usuarios.api.permissions import PermisoPorRol
from rest_framework.decorators import action
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.units import inch
from datetime import datetime

class LoteViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrRead, PermisoPorRol] 
    serializer_class = LoteSerializer
    
    def get_queryset(self):
        if self.action == 'reporte_pdf':
            return Lote.objects.filter(activo=True)
        return Lote.objects.all()
    
    @action(detail=False, methods=['get'])
    def reporte_pdf(self, request):
        lotes = self.get_queryset()
        
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="reporte_lotes.pdf"'

        doc = SimpleDocTemplate(response, pagesize=letter)
        elementos = []

        styles = getSampleStyleSheet()
        
        logo_path = "media/logo/def_AGROSIS_LOGOTIC.png" 
        logo = Image(logo_path, width=50, height=35)

        encabezado_data = [
            [logo, Paragraph("<b>Centro de gestión y desarrollo sostenible surcolombiano<br/>SENA - YAMBORÓ</b>", styles['Normal']), ""],
            ["", Paragraph("<b>Informe de Lotes Activos</b>", styles['Heading2']), Paragraph(f"{datetime.today().strftime('%Y-%m-%d')}", styles['Normal'])],
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

        elementos.append(Paragraph("<b>1. Objetivo</b>", styles['Heading2']))
        objetivo_texto = "Este documento presenta un reporte detallado de los lotes activos registrados en el sistema, incluyendo información sobre dimensiones, ubicación y características relevantes para la gestión agrícola."
        elementos.append(Paragraph(objetivo_texto, styles['Normal']))
        elementos.append(Spacer(1, 15))

        elementos.append(Paragraph("<b>2. Detalle de Lotes</b>", styles['Heading2']))
        
        data_lotes = [["Nombre", "Dimensiones (m)", "Ubicación", "Superficie (m²)", "Estado"]]
        for lote in lotes:
            data_lotes.append([
                lote.nombre,
                f"{lote.tam_x} x {lote.tam_y}",
                f"X: {lote.pos_x}, Y: {lote.pos_y}",
                f"{(lote.tam_x * lote.tam_y):.2f}",
                "Activo" 
            ])

        tabla_lotes = Table(data_lotes, colWidths=[80, 80, 100, 80, 60])
        tabla_lotes.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.black),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elementos.append(tabla_lotes)
        elementos.append(Spacer(1, 20))
              
        elementos.append(Paragraph("<b>3. Resumen General</b>", styles['Heading2']))
        resumen_texto = f"""
        Total de lotes activos: {lotes.count()}<br/>
        Superficie total disponible: {sum(l.tam_x * l.tam_y for l in lotes):.2f} m²<br/>
        """
        elementos.append(Paragraph(resumen_texto, styles['Normal']))
        elementos.append(Spacer(1, 15))

        elementos.append(Paragraph("<b>4. Información Adicional por Lote</b>", styles['Heading2']))

        for lote in lotes:
            elementos.append(Paragraph(f"<b>Lote: {lote.nombre}</b>", styles['Heading3']))
            
            info_lote = f"""
            <b>Descripción:</b> {lote.descripcion or 'Sin descripción'}<br/>
            <b>Superficie disponible:</b> {(lote.tam_x * lote.tam_y):.2f} m²<br/>
            """
            elementos.append(Paragraph(info_lote, styles['Normal']))
            elementos.append(Spacer(1, 10))

        doc.build(elementos)
        return response