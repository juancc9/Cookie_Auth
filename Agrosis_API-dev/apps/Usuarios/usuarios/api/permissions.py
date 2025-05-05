from rest_framework.permissions import BasePermission
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrRead(BasePermission):
   
    def has_permission(self, request, view):
        if request.method == "GET":
            return True
        else:
            return request.user.is_staff



class PermisoPorRol(BasePermission):
    """
    Permisos por rol:
    - Invitado (rol_id = 1): solo GET
    - Pasante (rol_id = 2): GET y POST
    - Instructor (rol_id = 3): todos
    - Administrador (rol_id = 4): todos
    """

    def has_permission(self, request, view):
        user = request.user

        rol = getattr(user, 'rol_id', None)
        print(f"Evaluando permiso para: {user} (rol={rol}, staff={user.is_staff})")

        if not user.is_authenticated:
            return False

        try:
            rol = int(rol)
        except (TypeError, ValueError):
            return False

        # Admin o Instructor: acceso total
        if rol in [3, 4] :
            return True

        # Pasante: solo GET y POST
        if rol == 2:
            return request.method in ['GET', 'POST']

        # Invitado: solo lectura
        if rol == 1:
            return request.method in SAFE_METHODS  # ['GET', 'HEAD', 'OPTIONS']

        # Cualquier otro caso, denegar
        return False

