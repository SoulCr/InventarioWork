from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from rest_framework import viewsets

from .models import Producto, Categoria, MovimientoStock
from .forms import ProductoForm, MovimientoStockForm
from .serializers import CategoriaSerializer, ProductoSerializer, MovimientoStockSerializer


def lista_productos(request):
    productos = Producto.objects.all().order_by('nombre')

    busqueda = request.GET.get('q', '')
    if busqueda:
        productos = productos.filter(nombre__icontains=busqueda) | productos.filter(sku__icontains=busqueda)

    categoria_id = request.GET.get('categoria', '')
    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)

    paginator = Paginator(productos, 10)  # 10 productos por página
    pagina = request.GET.get('page')
    productos_pagina = paginator.get_page(pagina)

    return render(request, 'inventarioapp/lista_productos.html', {
        'productos': productos_pagina,
        'categorias': Categoria.objects.all(),
        'busqueda': busqueda,
        'categoria_id': categoria_id,
    })

def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto creado correctamente.')
            return redirect('lista_productos')
    else:
        form = ProductoForm()
    return render(request, 'inventarioapp/form_producto.html', {
        'form': form,
        'titulo': 'Nuevo producto'
    })

def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado correctamente.')
            return redirect('lista_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'inventarioapp/form_producto.html', {
        'form': form,
        'titulo': 'Editar producto'
    })

def crear_movimiento(request):
    if request.method == 'POST':
        form = MovimientoStockForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Movimiento registrado correctamente.')
                return redirect('lista_productos')
            except ValidationError as e:
                form.add_error(None, e)
    else:
        form = MovimientoStockForm()
    return render(request, 'inventarioapp/form_movimiento.html', {
        'form': form
    })


#API
class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class MovimientoStockViewSet(viewsets.ModelViewSet):
    queryset = MovimientoStock.objects.all()
    serializer_class = MovimientoStockSerializer