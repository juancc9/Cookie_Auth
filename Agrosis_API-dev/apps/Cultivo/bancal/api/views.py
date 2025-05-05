from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from apps.Cultivo.bancal.models import Bancal
from apps.Cultivo.bancal.api.serializers import BancalSerializer
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
import os
from django.conf import settings

class BancalViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrRead,PermisoPorRol] 
    serializer_class = BancalSerializer
    
    def get_queryset(self):
        return Bancal.objects.all().order_by('nombre')
    
    @action(detail=False, methods=['get'])
    def reporte_pdf(self, request):
        bancales = self.get_queryset()
        
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="reporte_bancales.pdf"'

        doc = SimpleDocTemplate(response, pagesize=letter)
        elementos = []

        styles = getSampleStyleSheet()
        
        logo_path = os.path.join(settings.MEDIA_ROOT, 'logo', 'def_AGROSIS_LOGOTIC.png')
        logo = Image(logo_path, width=50, height=35) if os.path.exists(logo_path) else None

        encabezado_data = [
            [logo, Paragraph("<b>Centro de gestión y desarrollo sostenible surcolombiano<br/>SENA - YAMBORÓ</b>", styles['Normal']), ""],
            ["", Paragraph("<b>Reporte de Eras/Bancales</b>", styles['Heading2']), Paragraph(f"{datetime.today().strftime('%Y-%m-%d')}", styles['Normal'])],
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
        objetivo_texto = "Este documento presenta un reporte detallado de las eras/bancales registrados en el sistema, incluyendo información sobre dimensiones, ubicación y lote al que pertenecen."
        elementos.append(Paragraph(objetivo_texto, styles['Normal']))
        elementos.append(Spacer(1, 15))

        elementos.append(Paragraph("<b>2. Detalle de Eras/Bancales</b>", styles['Heading2']))
        
        data_bancales = [["Nombre", "Dimensiones (m)", "Ubicación", "Lote Asociado"]]
        for bancal in bancales:
            data_bancales.append([
                bancal.nombre,
                f"{bancal.TamX} x {bancal.TamY}" if bancal.TamX and bancal.TamY else "No definido",
                f"X: {bancal.posX}, Y: {bancal.posY}" if bancal.posX and bancal.posY else "No definido",
                bancal.lote.nombre if bancal.lote else "Sin lote"
            ])

        tabla_bancales = Table(data_bancales, colWidths=[100, 100, 120, 120])
        tabla_bancales.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.black),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elementos.append(tabla_bancales)
        elementos.append(Spacer(1, 20))
              
        elementos.append(Paragraph("<b>3. Resumen General</b>", styles['Heading2']))
        
        superficie_total = sum(
            float(bancal.TamX) * float(bancal.TamY) 
            for bancal in bancales 
            if bancal.TamX is not None and bancal.TamY is not None
        )
        
        resumen_texto = f"""
        Total de eras/bancales: {bancales.count()}<br/>
        Superficie total: {superficie_total:.2f} m²<br/>
        """
        elementos.append(Paragraph(resumen_texto, styles['Normal']))
        elementos.append(Spacer(1, 15))

        elementos.append(Paragraph("<b>4. Información Adicional por Era/Bancal</b>", styles['Heading2']))

        for bancal in bancales:
            elementos.append(Paragraph(f"<b>Era/Bancal: {bancal.nombre}</b>", styles['Heading3']))
            
            superficie = "No definida"
            if bancal.TamX is not None and bancal.TamY is not None:
                superficie = f"{(float(bancal.TamX) * float(bancal.TamY)):.2f} m²"
            
            info_bancal = f"""
            <b>Lote asociado:</b> {bancal.lote.nombre if bancal.lote else 'No asignado'}<br/>
            <b>Superficie:</b> {superficie}<br/>
            <b>Ubicación exacta:</b> X={bancal.posX if bancal.posX else 'ND'}, Y={bancal.posY if bancal.posY else 'ND'}<br/>
            """
            elementos.append(Paragraph(info_bancal, styles['Normal']))
            elementos.append(Spacer(1, 10))

        doc.build(elementos)
        return response