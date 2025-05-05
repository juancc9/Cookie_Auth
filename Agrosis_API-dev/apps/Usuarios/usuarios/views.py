from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from apps.Usuarios.usuarios.models import Usuarios, PasswordResetToken
from apps.Usuarios.usuarios.api.serializer import UsuariosSerializer, RegistroUsuarioSerializer
from django.core.mail import send_mail
from django.utils.crypto import get_random_string

class UsuariosViewSet(ModelViewSet):
    queryset = Usuarios.objects.all()
    serializer_class = UsuariosSerializer

class RegistroUsuarioView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistroUsuarioSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data

            # Encripta la contraseña antes de guardar el usuario
            usuario = Usuarios(
                nombre=validated_data['nombre'],
                apellido=validated_data['apellido'],
                email=validated_data['email'],
                username=validated_data['username'],
                rol=validated_data.get('rol')  # Puede ser None
            )
            usuario.set_password(validated_data['password'])  # Encripta correctamente la contraseña
            usuario.save()

            return Response(UsuariosSerializer(usuario).data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]
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
                'steventu06@gmail.com',
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