from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'api/categorias', views.CategoriaViewSet)
router.register(r'api/productos', views.ProductoViewSet)
router.register(r'api/movimientos', views.MovimientoStockViewSet)

urlpatterns = [
    path('', views.lista_productos, name='lista_productos'),
    path('productos/nuevo/', views.crear_producto, name='crear_producto'),
    path('productos/<int:pk>/editar/', views.editar_producto, name='editar_producto'),
    path('movimientos/nuevo/', views.crear_movimiento, name='crear_movimiento'),
    path('', include(router.urls)),
]