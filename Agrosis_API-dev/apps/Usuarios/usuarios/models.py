from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.Usuarios.roles.models import Roles
from django.utils import timezone
from datetime import timedelta

class Usuarios(AbstractUser): 
    rol = models.ForeignKey(Roles, on_delete=models.SET_NULL, null=True, blank=True, default=1)
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = ['username', 'nombre', 'apellido'] 

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class PasswordResetToken(models.Model):
    user = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    token = models.CharField(max_length=32, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(hours=24)  

    def __str__(self):
        return f"Token para {self.user.email}"