from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from apps.Usuarios.usuarios.api.views import (RegistroUsuarioView, CurrentUserView, PasswordResetRequestView, PasswordResetConfirmView, ChangePasswordView)
from apps.Usuarios.usuarios.api.routers import UsuariosRouter
from apps.Usuarios.roles.api.routers import RolesRouter
from apps.Cultivo.actividades.api.router import actividadRouter 
from apps.Cultivo.afecciones.api.router import afeccionRouter 
from apps.Cultivo.bancal.api.router import bancalRouter 
from apps.Cultivo.controles.api.router import controlRouter 
from apps.Cultivo.cosechas.api.router import cosechaRouter 
from apps.Cultivo.cultivos.api.router import cultivoRouter 
from apps.Cultivo.especies.api.router import especiesRouter 
from apps.Cultivo.fase_lunar.api.router import faseLunarRouter 
from apps.Cultivo.lotes.api.router import lotesRouter 
from apps.Cultivo.plagas.api.router import plagasRouter 
from apps.Cultivo.plantaciones.api.router import plantacionRouter 
from apps.Cultivo.productos_control.api.router import productosControlRouter 
from apps.Cultivo.programacion.api.router import programacionRouter 
from apps.Cultivo.residuos.api.router import residuosRouter 
from apps.Cultivo.semillero.api.router import semilleroRouter 
from apps.Cultivo.tipo_actividad.api.router import tipoActividadRouter 
from apps.Cultivo.tipo_control.api.router import tipoControlRouter 
from apps.Cultivo.tipo_especies.api.router import tipoEspecieRouter 
from apps.Cultivo.tipo_plaga.api.router import tipoPlagaRouter 
from apps.Cultivo.tipos_residuos.api.router import tipoResiduoRouter 
from apps.Cultivo.tareas.api.router import tareaRouter
from apps.Cultivo.ReportePlaga.api.router import reporte_plaga_router
from apps.Finanzas.pagos.api.router import pagoRouter
from apps.Finanzas.salario.api.router import salarioRouter
from apps.Finanzas.venta.api.router import ventaRouter
from apps.Inventario.herramientas.api.routers import herramientaRouter
from apps.Inventario.insumos.api.routers import insumoRouter
from apps.Inventario.precio_producto.api.routers import precioProductoRouter
from apps.Inventario.bodega.api.routers import bodegaRouter
from apps.Inventario.bodega_insumo.api.routers import bodegaInsumoRouter
from apps.Inventario.bodega_herramienta.api.routers import bodegaHerramientaRouter
from apps.Iot.datos_meteorologicos.api.routers import DatosMeteorologicosRouter  
from apps.Iot.sensores.api.routers import SensoresRouter
from apps.Iot.evapotranspiracion.api.routers import evapotranspiracionrouter
from apps.Autenticacion.autenticacion.api.views import CustomLoginView

schema_view = get_schema_view(
    openapi.Info(
        title="Documentación API",
        default_version='v0.1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)

router = DefaultRouter()
routerUsuarios = DefaultRouter()
routerCultivo = DefaultRouter()
routerFinanzas = DefaultRouter()
routerInventario = DefaultRouter()
routerIOT = DefaultRouter()

# Usuarios
routerUsuarios.registry.extend(UsuariosRouter.registry)
routerUsuarios.registry.extend(RolesRouter.registry)

# Cultivo
routerCultivo.registry.extend(actividadRouter.registry)
routerCultivo.registry.extend(afeccionRouter.registry)
routerCultivo.registry.extend(bancalRouter.registry)
routerCultivo.registry.extend(controlRouter.registry)
routerCultivo.registry.extend(cosechaRouter.registry)
routerCultivo.registry.extend(cultivoRouter.registry)
routerCultivo.registry.extend(especiesRouter.registry)
routerCultivo.registry.extend(faseLunarRouter.registry)
routerCultivo.registry.extend(lotesRouter.registry)
routerCultivo.registry.extend(plagasRouter.registry)
routerCultivo.registry.extend(plantacionRouter.registry)
routerCultivo.registry.extend(productosControlRouter.registry)
routerCultivo.registry.extend(programacionRouter.registry)
routerCultivo.registry.extend(residuosRouter.registry)
routerCultivo.registry.extend(semilleroRouter.registry)
routerCultivo.registry.extend(tipoActividadRouter.registry)
routerCultivo.registry.extend(tipoControlRouter.registry)
routerCultivo.registry.extend(tipoEspecieRouter.registry)
routerCultivo.registry.extend(tipoPlagaRouter.registry)
routerCultivo.registry.extend(tipoResiduoRouter.registry)
routerCultivo.registry.extend(tareaRouter.registry)
routerCultivo.registry.extend(reporte_plaga_router.registry)
# Finanzas
routerFinanzas.registry.extend(pagoRouter.registry)
routerFinanzas.registry.extend(salarioRouter.registry)
routerFinanzas.registry.extend(ventaRouter.registry)

# Inventario
routerInventario.registry.extend(herramientaRouter.registry)
routerInventario.registry.extend(insumoRouter.registry)
routerInventario.registry.extend(precioProductoRouter.registry)
routerInventario.registry.extend(bodegaRouter.registry)
routerInventario.registry.extend(bodegaInsumoRouter.registry)
routerInventario.registry.extend(bodegaHerramientaRouter.registry)

# IOT
routerIOT.registry.extend(DatosMeteorologicosRouter.registry) 
routerIOT.registry.extend(SensoresRouter.registry)
routerIOT.registry.extend(evapotranspiracionrouter.registry)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/', include(router.urls)),
    path('usuarios/', include(routerUsuarios.urls)),
    path('cultivo/', include(routerCultivo.urls)),
    path('iot/', include(routerIOT.urls)),
    path('finanzas/', include(routerFinanzas.urls)),
    path('inventario/', include(routerInventario.urls)),
    path('usuarios/registro/', RegistroUsuarioView.as_view(), name='registro_usuario'),
    path('usuarios/me/', CurrentUserView.as_view(), name='current_user'),
    path('usuarios/password_reset/', PasswordResetRequestView.as_view(), name='password_reset'),
    path('usuarios/change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('usuarios/password_reset_confirm/<str:token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('auth/login/', CustomLoginView.as_view(), name='auth'),
    # path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
]   