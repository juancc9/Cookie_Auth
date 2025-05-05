from django.urls import path
from .api.routers import roles_urlpatterns

app_name = 'roles'

urlpatterns = [] + roles_urlpatterns