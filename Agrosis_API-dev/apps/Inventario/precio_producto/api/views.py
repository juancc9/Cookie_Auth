from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.units import inch
from datetime import datetime
from apps.Inventario.insumos.models import UnidadMedida
from apps.Usuarios.usuarios.api.permissions import PermisoPorRol
from ..models import PrecioProducto
from .serializers import PrecioProductoSerializer, UnidadMedidaSerializer

class PrecioProductoViewSet(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, PermisoPorRol]
    queryset = PrecioProducto.objects.all().select_related('unidad_medida', 'Producto')
    serializer_class = PrecioProductoSerializer

    @action(detail=True, methods=['post'])
    def registrar_venta(self, request, pk=None):
        producto = self.get_object()
        cantidad_vendida = request.data.get('cantidad', 0)

        try:
            cantidad_vendida = int(cantidad_vendida)
            if cantidad_vendida <= 0:
                return Response({"error": "La cantidad debe ser mayor a 0."}, status=status.HTTP_400_BAD_REQUEST)
            if cantidad_vendida > producto.stock:
                return Response({"error": "No hay suficiente stock disponible."}, status=status.HTTP_400_BAD_REQUEST)

            producto.stock -= cantidad_vendida
            producto.save()
            return Response({"mensaje": f"Venta registrada. Stock actual: {producto.stock}"}, status=status.HTTP_200_OK)
        except ValueError:
            return Response({"error": "Cantidad inválida."}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def unidades_medida(self, request):
        unidades = UnidadMedida.objects.all()
        serializer = UnidadMedidaSerializer(unidades, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def crear_unidad_medida(self, request):
        serializer = UnidadMedidaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(creada_por_usuario=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def reporte_pdf(self, request):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="reporte_precios_productos.pdf"'

        doc = SimpleDocTemplate(response, pagesize=letter)
        elementos = []
        styles = getSampleStyleSheet()

        logo_path = "media/logo/def_AGROSIS_LOGOTIC.png"
        logo = Image(logo_path, width=50, height=35)
        encabezado_data = [
            [logo, Paragraph("<b>Empresa XYZ</b><br/>Reporte de Precios de Productos", styles['Normal']), ""],
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
            "Este documento detalla los precios, stock y fechas de caducidad de productos registrados en el sistema.",
            styles['Normal'])
        )
        elementos.append(Spacer(1, 15))

        elementos.append(Paragraph("<b>2. Registro de Precios de Productos</b>", styles['Heading2']))
        elementos.append(Spacer(1, 5))

        precios = self.get_queryset()
        total_precios = precios.count()
        suma_precios = sum(float(precio.precio) for precio in precios)

        data_precios = [
            ["ID", "Producto", "Unidad de Medida", "Precio", "Fecha Registro", "Stock", "Fecha Caducidad"]
        ]
        for precio in precios:
            fecha_registro = precio.fecha_registro.strftime('%Y-%m-%d')
            fecha_caducidad = precio.fecha_caducidad.strftime('%Y-%m-%d') if precio.fecha_caducidad else "N/A"
            unidad_medida = precio.unidad_medida.nombre if precio.unidad_medida else "Sin asignar"
            data_precios.append([
                str(precio.id),
                str(precio.Producto) if precio.Producto else "Sin producto",
                unidad_medida,
                f"{precio.precio:.2f}",
                fecha_registro,
                str(precio.stock),
                fecha_caducidad
            ])

        tabla_precios = Table(data_precios, colWidths=[30, 150, 70, 50, 70, 50, 70])
        tabla_precios.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.black),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 7),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 1), (-1, -1), 'MIDDLE'),
            ('WORDWRAP', (0, 0), (-1, -1), 'CJK'),
        ]))
        elementos.append(tabla_precios)
        elementos.append(Spacer(1, 15))

        elementos.append(Paragraph("<b>3. Resumen General</b>", styles['Heading2']))
        resumen_texto = f"""
        Se registraron {total_precios} precios de productos en el sistema,
        con un total acumulado de {suma_precios:.2f} en precios.
        """
        elementos.append(Paragraph(resumen_texto, styles['Normal']))

        doc.build(elementos)
        return response