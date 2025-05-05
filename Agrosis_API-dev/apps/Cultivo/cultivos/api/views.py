from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from apps.Cultivo.cultivos.models import Cultivo
from apps.Cultivo.cultivos.api.serializers import CultivoSerializer
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

class CultivoViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrRead, PermisoPorRol] 
    serializer_class = CultivoSerializer
    
    def get_queryset(self):
        queryset = Cultivo.objects.all()
        
        mostrar_inactivos = self.request.query_params.get('activo', '').lower() == 'false'
        
        if not mostrar_inactivos:
            queryset = queryset.filter(activo=True)
        return queryset
    
    @action(detail=False, methods=['get'])
    def reporte_cultivos_activos(self, request):
        fecha_inicio = request.GET.get('fecha_inicio')
        fecha_fin = request.GET.get('fecha_fin')
        
        cultivos = self.get_queryset()
        
        if fecha_inicio and fecha_fin:
            cultivos = cultivos.filter(
                fechaSiembra__range=[fecha_inicio, fecha_fin]
            )
        
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="reporte_cultivos_activos.pdf"'

        doc = SimpleDocTemplate(response, pagesize=letter)
        elementos = []

        styles = getSampleStyleSheet()
        
        logo_path = "media/logo/def_AGROSIS_LOGOTIC.png" 
        logo = Image(logo_path, width=50, height=35)

        encabezado_data = [
            [logo, Paragraph("<b>Centro de gestión y desarrollo sostenible surcolombiano<br/>SENA - YAMBORÓ</b>", styles['Normal']), ""],
            ["", Paragraph("<b>Reporte de Cultivos Activos</b>", styles['Heading2']), Paragraph(f"{datetime.today().strftime('%Y-%m-%d')}", styles['Normal'])],
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
        objetivo_texto = "Este documento presenta un reporte detallado de los cultivos activos registrados en el sistema, incluyendo información clave para la gestión agrícola como especies, ubicación, fechas de siembra y estado actual."
        elementos.append(Paragraph(objetivo_texto, styles['Normal']))
        elementos.append(Spacer(1, 15))

        elementos.append(Paragraph("<b>2. Resumen General</b>", styles['Heading2']))
        resumen_texto = f"""
        Total de cultivos activos: {cultivos.count()}<br/>
        Rango de fechas: {fecha_inicio or 'No especificado'} a {fecha_fin or 'No especificado'}<br/>
        """
        elementos.append(Paragraph(resumen_texto, styles['Normal']))
        elementos.append(Spacer(1, 15))

        elementos.append(Paragraph("<b>3. Detalle de Cultivos Activos</b>", styles['Heading2']))
        
        data_cultivos = [["Nombre", "Especie", "Bancal", "Fecha Siembra", "Unidad Medida"]]
        for cultivo in cultivos:
            data_cultivos.append([
                cultivo.nombre,
                cultivo.Especie.nombre if cultivo.Especie else "N/A",
                cultivo.Bancal.nombre if cultivo.Bancal else "N/A",
                cultivo.fechaSiembra.strftime("%Y-%m-%d"),
                cultivo.unidad_de_medida or "N/A"
            ])

        tabla_cultivos = Table(data_cultivos, colWidths=[100, 100, 80, 80, 60])
        tabla_cultivos.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.black),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elementos.append(tabla_cultivos)
        elementos.append(Spacer(1, 20))

        elementos.append(Paragraph("<b>4. Información Adicional</b>", styles['Heading2']))
        elementos.append(Paragraph("""
        <b>Estado:</b> Todos los cultivos listados se encuentran en estado activo.<br/>
        <b>Notas:</b> Para más detalles sobre cada cultivo, consulte el sistema de gestión agrícola.
        """, styles['Normal']))

        doc.build(elementos)
        return response
