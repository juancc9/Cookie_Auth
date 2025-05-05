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
from apps.Usuarios.usuarios.api.permissions import PermisoPorRol
from ..models import Insumo, UnidadMedida, TipoInsumo
from apps.Cultivo.actividades.models import Actividad
from .serializers import InsumoSerializer, UnidadMedidaSerializer, TipoInsumoSerializer


class InsumoViewSet(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, PermisoPorRol]
    queryset = Insumo.objects.all()
    serializer_class = InsumoSerializer

    @action(detail=True, methods=["post"])
    def usar_en_actividad(self, request, pk=None):
        insumo = self.get_object()
        cantidad_usada = request.data.get("cantidad_usada", 0)
        actividad_id = request.data.get("actividad_id", None)

        try:
            cantidad_usada = int(cantidad_usada)
            if cantidad_usada <= 0:
                return Response(
                    {"error": "La cantidad usada debe ser mayor a 0."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if cantidad_usada > insumo.cantidad:
                return Response(
                    {
                        "error": f"No hay suficiente stock del insumo {insumo.nombre}. Disponible: {insumo.cantidad}"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            insumo.cantidad -= cantidad_usada
            insumo.save()

            if actividad_id:
                try:
                    actividad = Actividad.objects.get(id=actividad_id)
                    if actividad.insumo != insumo:
                        return Response(
                            {
                                "error": f"El insumo {insumo.nombre} no coincide con el insumo de la actividad {actividad_id}."
                            },
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                    actividad.cantidadUsada += cantidad_usada
                    actividad.save()
                    mensaje = f"Insumo {insumo.nombre} descontado ({cantidad_usada} unidades) y vinculado a la actividad {actividad.id}."
                except Actividad.DoesNotExist:
                    return Response(
                        {"error": f"La actividad {actividad_id} no existe."},
                        status=status.HTTP_404_NOT_FOUND,
                    )
            else:
                mensaje = f"Insumo {insumo.nombre} descontado ({cantidad_usada} unidades) sin vinculación a una actividad específica."

            return Response(
                {"mensaje": mensaje, "cantidad_restante": insumo.cantidad},
                status=status.HTTP_200_OK,
            )

        except ValueError:
            return Response(
                {"error": "Cantidad inválida."}, status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=["get"])
    def reporte_pdf(self, request):
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="reporte_insumos.pdf"'

        doc = SimpleDocTemplate(response, pagesize=letter)
        elementos = []
        styles = getSampleStyleSheet()

        logo_path = "media/logo/def_AGROSIS_LOGOTIC.png"
        logo = Image(logo_path, width=50, height=35)
        encabezado_data = [
            [
                logo,
                Paragraph(
                    "<b>Empresa XYZ</b><br/>Reporte de Insumos", styles["Normal"]
                ),
                "",
            ],
            [
                "",
                Paragraph(
                    f"Fecha: {datetime.today().strftime('%Y-%m-%d')}",
                    styles["Normal"],
                ),
                "Página 1",
            ],
        ]

        tabla_encabezado = Table(encabezado_data, colWidths=[60, 350, 100])
        tabla_encabezado.setStyle(
            TableStyle(
                [
                    ("SPAN", (0, 0), (0, 1)),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ]
            )
        )
        elementos.append(tabla_encabezado)

        elementos.append(Spacer(1, 10))

        elementos.append(Paragraph("<b>1. Objetivo</b>", styles["Heading2"]))
        elementos.append(
            Paragraph(
                "Este documento detalla los insumos registrados en el sistema, facilitando su gestión y permitiendo un control eficiente sobre los recursos disponibles.",
                styles["Normal"],
            )
        )
        elementos.append(Spacer(1, 15))

        elementos.append(Paragraph("<b>2. Inventario de Insumos</b>", styles["Heading2"]))
        elementos.append(Spacer(1, 5))

        insumos = Insumo.objects.all()
        total_insumos = insumos.count()
        cantidad_total = sum(insumo.cantidad for insumo in insumos)

        data_insumos = [
            [
                "ID",
                "Nombre",
                "Descripción",
                "Cantidad",
                "U de Medida",
                "T Insumo",
                "T Empacado",
                "F Registro",
                "F Caducidad",
                "Activo",
                "Precio",
                "Compuesto",
            ]
        ]
        for insumo in insumos:
            fecha_registro = (
                insumo.fecha_registro.strftime("%Y-%m-%d %H:%M")
                if insumo.fecha_registro
                else "N/A"
            )
            fecha_caducidad = (
                insumo.fecha_caducidad.strftime("%Y-%m-%d")
                if insumo.fecha_caducidad
                else "N/A"
            )
            unidad_medida = (
                insumo.unidad_medida.nombre if insumo.unidad_medida else "Sin asignar"
            )
            tipo_insumo = (
                insumo.tipo_insumo.nombre if insumo.tipo_insumo else "Sin asignar"
            )
            data_insumos.append(
                [
                    str(insumo.id),
                    insumo.nombre,
                    insumo.descripcion,
                    str(insumo.cantidad),
                    unidad_medida,
                    tipo_insumo,
                    insumo.tipo_empacado if insumo.tipo_empacado else "N/A",
                    fecha_registro,
                    fecha_caducidad,
                    "Sí" if insumo.activo else "No",
                    str(insumo.precio_insumo),
                    "Sí" if insumo.es_compuesto else "No",
                ]
            )

        tabla_insumos = Table(
            data_insumos, colWidths=[30, 60, 80, 40, 50, 50, 50, 80, 50, 30, 50, 30]
        )
        tabla_insumos.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.black),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, -1), 7),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ("VALIGN", (0, 1), (-1, -1), "MIDDLE"),
                    ("WORDWRAP", (0, 0), (-1, -1), "CJK"),
                ]
            )
        )
        elementos.append(tabla_insumos)
        elementos.append(Spacer(1, 15))

        elementos.append(Paragraph("<b>3. Resumen General</b>", styles["Heading2"]))
        resumen_texto = f"""
        Se registraron {total_insumos} insumos en el sistema,
        con un total acumulado de {cantidad_total} unidades.
        """
        elementos.append(Paragraph(resumen_texto, styles["Normal"]))

        doc.build(elementos)
        return response

    @action(detail=False, methods=["get"])
    def unidades_medida(self, request):
        unidades = UnidadMedida.objects.all()
        serializer = UnidadMedidaSerializer(unidades, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["post"])
    def crear_unidad_medida(self, request):
        serializer = UnidadMedidaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(creada_por_usuario=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"])
    def tipos_insumo(self, request):
        tipos = TipoInsumo.objects.all()
        serializer = TipoInsumoSerializer(tipos, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["post"])
    def crear_tipo_insumo(self, request):
        serializer = TipoInsumoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(creada_por_usuario=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)