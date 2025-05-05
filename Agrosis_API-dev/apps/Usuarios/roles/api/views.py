from rest_framework.viewsets import ModelViewSet
from apps.Usuarios.roles.models import Roles
from apps.Usuarios.roles.api.serializer import RolSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class RolViewSet(ModelViewSet):
    queryset = Roles.objects.all()
    serializer_class = RolSerializer
    permission_classes = [IsAuthenticated]  
    def get(self, request):
        roles = Roles.objects.all()
        serializer = RolSerializer(roles, many=True)
        return Response(serializer.data)


