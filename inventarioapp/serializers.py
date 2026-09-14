from rest_framework import serializers
from .models import Categoria, Producto, MovimientoStock

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre']

class ProductoSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    necesita_reposicion = serializers.BooleanField(read_only=True)

    class Meta:
        model = Producto
        fields = [
            'id', 'nombre', 'sku', 'categoria', 'categoria_nombre',
            'precio_costo', 'precio_venta', 'stock_actual', 'stock_minimo',
            'necesita_reposicion',
        ]

class MovimientoStockSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)

    class Meta:
        model = MovimientoStock
        fields = ['id', 'producto', 'producto_nombre', 'tipo', 'cantidad', 'motivo', 'fecha']
        read_only_fields = ['fecha']