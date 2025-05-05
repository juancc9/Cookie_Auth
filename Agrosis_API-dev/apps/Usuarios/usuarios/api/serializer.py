from rest_framework import serializers
from apps.Usuarios.usuarios.models import Usuarios
from apps.Usuarios.roles.models import Roles
from apps.Usuarios.roles.api.serializer import RolSerializer
from rest_framework.validators import UniqueValidator


class UsuariosSerializer(serializers.ModelSerializer):
    rol = RolSerializer(read_only=True)
    rol_id = serializers.PrimaryKeyRelatedField(
        queryset=Roles.objects.all(), source="rol", write_only=True, allow_null=True
    )

    class Meta:
        model = Usuarios
        fields = ['id', 'nombre', 'apellido', 'email', 'username', 'rol', 'rol_id']

    def update(self, instance, validated_data):
        nuevo_rol = validated_data.get("rol", instance.rol)

        # Si el rol es 4, asignar is_superuser e is_staff a True
        if nuevo_rol and nuevo_rol.id == 4:
            instance.is_superuser = True
            instance.is_staff = True
        else:
            instance.is_superuser = False
            instance.is_staff = False

        instance = super().update(instance, validated_data)
        instance.save(update_fields=["is_superuser", "is_staff"])
        return instance


class RegistroUsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        style={'input_type': 'password'}
    )
    
    email = serializers.EmailField(
        validators=[UniqueValidator(
            queryset=Usuarios.objects.all(),
            message="Ya existe un usuario con ese correo electrónico."
        )]
    )
    
    username = serializers.CharField(
        validators=[UniqueValidator(
            queryset=Usuarios.objects.all(),
            message="Ya existe un usuario con ese nombre de usuario."
        )]
    )

    class Meta:
        model = Usuarios
        fields = ['id', 'nombre', 'apellido', 'email', 'username', 'rol', 'password']

    def create(self, validated_data):
        print("Entró al create del RegistroUsuarioSerializer")

        if 'password' not in validated_data:
            raise serializers.ValidationError({"password": "Este campo es obligatorio."})

        password = validated_data.pop('password')
        usuario = Usuarios(**validated_data)

        # Siempre asignar permisos de superusuario y staff
        usuario.is_superuser = True
        usuario.is_staff = True

        usuario.set_password(password)
        usuario.save()
        return usuario
