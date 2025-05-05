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
from apps.Usuarios.usuarios.api.permissions import PermisoPorRol
from ..models import Herramienta
from .serializers import HerramientaSerializer

class HerramientaViewSet(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, PermisoPorRol]
    queryset = Herramienta.objects.all()
    serializer_class = HerramientaSerializer

    @action(detail=False, methods=['get'])
    def reporte_pdf(self, request):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="reporte_herramientas.pdf"'

        doc = SimpleDocTemplate(response, pagesize=letter)
        elementos = []
        styles = getSampleStyleSheet()

        logo_path = "media/logo/def_AGROSIS_LOGOTIC.png"
        logo = Image(logo_path, width=50, height=35)
        encabezado_data = [
            [logo, Paragraph("<b>Empresa XYZ</b><br/>Reporte de Herramientas", styles['Normal']), ""],
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
            "Este documento detalla las herramientas registradas en el sistema, facilitando su gestión y permitiendo un control eficiente sobre los recursos disponibles.",
            styles['Normal'])
        )
        elementos.append(Spacer(1, 15))

        elementos.append(Paragraph("<b>2. Inventario de Herramientas</b>", styles['Heading2']))
        elementos.append(Spacer(1, 5))

        herramientas = Herramienta.objects.all()
        total_herramientas = herramientas.count()
        cantidad_total = sum(herramienta.cantidad for herramienta in herramientas)

        data_herramientas = [
            ["ID", "Nombre", "Descripción", "Cantidad", "Estado", "Activo", "Fecha Registro"]
        ]
        for herramienta in herramientas:
            fecha_registro = herramienta.fecha_registro.strftime('%Y-%m-%d %H:%M') if herramienta.fecha_registro else "N/A"
            data_herramientas.append([
                str(herramienta.id),
                herramienta.nombre,
                herramienta.descripcion,
                str(herramienta.cantidad),
                herramienta.estado,
                "Sí" if herramienta.activo else "No",
                fecha_registro
            ])

        tabla_herramientas = Table(data_herramientas, colWidths=[30, 80, 120, 40, 50, 40, 70])
        tabla_herramientas.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.black),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 7),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 1), (-1, -1), 'MIDDLE'),
            ('WORDWRAP', (0, 0), (-1, -1), 'CJK'),
        ]))
        elementos.append(tabla_herramientas)
        elementos.append(Spacer(1, 15))

        elementos.append(Paragraph("<b>3. Resumen General</b>", styles['Heading2']))
        resumen_texto = f"""
        Se registraron {total_herramientas} herramientas en el sistema,
        con un total acumulado de {cantidad_total} unidades.
        """
        elementos.append(Paragraph(resumen_texto, styles['Normal']))

        doc.build(elementos)
        return response