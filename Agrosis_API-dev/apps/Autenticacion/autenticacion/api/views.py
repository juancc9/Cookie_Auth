from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from datetime import timedelta
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status



class CustomLoginView(TokenObtainPairView):
    def post(self, request):
        print("🟠🟠AUTHCOOKIE")
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(username=email, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            res = Response({"message": "Login successful"}, status=status.HTTP_200_OK)

            # Seteamos cookie segura con el token
            res.set_cookie(   # <-- antes decía response.set_cookie
                key='access_token',
                value=access_token,   # <-- antes decía token
                httponly=True,
                secure=True,          # ⬅️ requerido para SameSite=None
                samesite='None',       # ⬅️ permite cross-site
            )
            return res
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutConCookieView(APIView):
    def post(self, request):
        response = Response({"message": "Sesión cerrada"}, status=200)

        # Eliminar las cookies de access_token y refresh_token
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")

        return response

