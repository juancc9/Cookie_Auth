from django.contrib import admin
from .models import Roles

@admin.register(Roles)
class RolesAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha_creacion', 'fecha_actualizacion')
    search_fields = ('nombre',)
    list_filter = ('nombre',)