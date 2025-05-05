from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import PermisoPorRol
from apps.Usuarios.usuarios.models import Usuarios, PasswordResetToken
from apps.Usuarios.usuarios.api.serializer import UsuariosSerializer, RegistroUsuarioSerializer
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from rest_framework.decorators import action
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from django.http import HttpResponse
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib import colors
from django.utils.timezone import make_aware
from django.utils import timezone
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.exceptions import AuthenticationFailed



hoy = datetime.today()

inicio_año = datetime(hoy.year, 1, 1)




class UsuariosViewSet(ModelViewSet):
    print("Agrege permisoporRol")
    serializer_class = UsuariosSerializer
    queryset = Usuarios.objects.all()
    permission_classes = [IsAuthenticated, PermisoPorRol]

    
    @action(detail=False, methods=['get'])
    def reporte_pdf(self, request):

         fecha_inicio = request.GET.get('fecha_inicio')
         fecha_fin = request.GET.get('fecha_fin')
 
         if not fecha_inicio or not fecha_fin:
             return HttpResponse("Error: Debes proporcionar 'fecha_inicio' y 'fecha_fin'", status=400)
 
         fecha_inicio = make_aware(inicio_año)
         fecha_fin = make_aware(hoy)
 
        #  usuarios = Usuarios.objects.filter(fecha__range=[fecha_inicio, fecha_fin])
         usuarios = Usuarios.objects.filter(date_joined__range=[fecha_inicio, fecha_fin])  # ✅ Usa 'date_joined'


         total_usuarios = usuarios.count()
         promedio_usuarios = total_usuarios  # Solo tiene sentido contar, no sumar
         response = HttpResponse(content_type='application/pdf')

         response['Content-Disposition'] = 'attachment; filename="reporte_de_usuarios.pdf"'
 
         doc = SimpleDocTemplate(response, pagesize=letter)
         elementos = []
         styles = getSampleStyleSheet()

         #Elemento visual
         logo_path = "media/logo/def_AGROSIS_LOGOTIC.png" 

         logo = Image(logo_path, width=50, height=35)
 
         encabezado_data = [
             [logo, Paragraph("<b>Centro de gestión y desarrollo sostenible surcolombiano<br/>SENA - YAMBORÓ</b>", styles['Normal']), ""],
             ["", Paragraph("<b>Informe de Usuarios activos</b>", styles['Heading2']), Paragraph(f"{datetime.today().strftime('%Y-%m-%d')}", styles['Normal'])],
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
 
 
 
         subtitulo = Paragraph("Informe de Usuarios Activos", styles['Heading2'])
         elementos.append(subtitulo)
         elementos.append(Spacer(1, 10))
 
         objetivo_texto = "Este documento presenta un resumen detallado de los Usuarios activos hasta la fecha en el sistema,incluyendo información de los mismos. El objetivo es proporcionar una visión general de los usuarios presentes en el sistema y control sobre sus roles."
         objetivo = Paragraph("<b>1. Objetivo</b><br/>" + objetivo_texto, styles['Normal'])
         elementos.append(objetivo)
         elementos.append(Spacer(1, 15))
 
         elementos.append(Paragraph("<b>2. Detalle de Usuarios activos</b>", styles['Heading3']))
         elementos.append(Spacer(1, 5))
 
         data_usuarios = [["nombre", "email", "rol","fecha de registro"]]
         for usuario in usuarios:
             print("Total de usuarios encontrados:", usuarios.count())
             data_usuarios.append([
                 usuario.nombre,
                 usuario.email,
                 usuario.rol.nombre,
                 usuario.date_joined.strftime("%Y-%m-%d")

             ])


         tabla_usuarios_activos = Table(data_usuarios)
         tabla_usuarios_activos.setStyle(TableStyle([
             ('BACKGROUND', (0, 0), (-1, 0), colors.black),
             ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
             ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
             ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
             ('GRID', (0, 0), (-1, -1), 1, colors.black),
         ]))

         elementos.append(tabla_usuarios_activos)
         elementos.append(Spacer(1, 15))

         elementos.append(Paragraph("<b>3. Resumen General</b>", styles['Heading3']))
         resumen_texto = f"""
         Durante el período del {fecha_inicio} al {fecha_fin}, se obtuvieron {total_usuarios} usuarios activos en el sistema. 
         """
         elementos.append(Paragraph(resumen_texto, styles['Normal']))
 
         doc.build(elementos)
 
         return response
    
class RegistroUsuarioView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        serializer = RegistroUsuarioSerializer(data=request.data)
        if serializer.is_valid():
            
            usuario = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]
    print("Currentuser🔴🔴")

    def get(self, request):
        user = request.user
        serializer = UsuariosSerializer(user)
        return Response(serializer.data)


class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'El correo es requerido'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = Usuarios.objects.get(email=email, is_active=True)
            token = get_random_string(length=32)
            PasswordResetToken.objects.create(user=user, token=token)
            reset_link = f"http://localhost:5173/reset-password/{token}/"
            send_mail(
                'Restablecer Contraseña',
                f'Haz clic aquí para restablecer tu contraseña: {reset_link}',
                'agrosoftadso2024@gmail.com',
                [email],
                fail_silently=False,
            )
            return Response({'message': 'Correo de recuperación enviado'}, status=status.HTTP_200_OK)
        except Usuarios.DoesNotExist:
            return Response({'error': 'Usuario no encontrado o inactivo'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Error del servidor: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, token):
        password = request.data.get('password')
        if not password:
            return Response({'error': 'La contraseña es requerida'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            reset_token = PasswordResetToken.objects.get(token=token)
            if reset_token.is_expired():
                reset_token.delete()
                return Response({'error': 'Token expirado'}, status=status.HTTP_400_BAD_REQUEST)
            user = reset_token.user
            user.set_password(password)
            user.save()
            reset_token.delete()
            return Response({'message': 'Contraseña restablecida con éxito'}, status=status.HTTP_200_OK)
        except PasswordResetToken.DoesNotExist:
            return Response({'error': 'Token inválido'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'Error del servidor: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')

        if not current_password or not new_password:
            return Response(
                {'error': 'Se requieren la contraseña actual y la nueva contraseña'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not user.check_password(current_password):
            return Response(
                {'error': 'La contraseña actual es incorrecta'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(new_password)
        user.save()
        return Response(
            {'message': 'Contraseña actualizada con éxito'},
            status=status.HTTP_200_OK
        )