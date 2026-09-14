from django.contrib import admin
from .models import Categoria, Producto , MovimientoStock
from django.utils.html import format_html


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'sku', 'categoria', 'precio_venta', 'stock_actual', 'stock_minimo', 'alerta')
    list_filter = ('categoria',)
    search_fields = ('nombre', 'sku')

    def alerta(self, obj):
        if obj.necesita_reposicion:
            return format_html('<span style="color: red; font-weight: bold;">{}</span>', '⚠ Reponer')
        return format_html('<span style="color: green;">{}</span>', 'OK')

    alerta.short_description = 'Stock'


@admin.register(MovimientoStock)
class MovimientoStockAdmin(admin.ModelAdmin):
    list_display = ('producto', 'tipo', 'cantidad', 'fecha')
    list_filter = ('tipo', 'fecha')
    search_fields = ('producto__nombre',)

from django.contrib import admin

# Register your models here.
