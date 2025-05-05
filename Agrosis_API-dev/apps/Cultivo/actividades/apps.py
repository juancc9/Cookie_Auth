from django.apps import AppConfig


class ActividadesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.Cultivo.actividades'
    
    def ready(self):
        import apps.Cultivo.actividades.api.signals