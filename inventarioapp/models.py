from django.db import models
from django.core.exceptions import ValidationError

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=150)
    sku = models.CharField(max_length=50, unique=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    precio_costo = models.DecimalField(max_digits=10, decimal_places=2)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    stock_actual = models.PositiveIntegerField(default=0)
    stock_minimo = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.nombre} ({self.sku})"

    @property
    def necesita_reposicion(self):
        return self.stock_actual <= self.stock_minimo


class MovimientoStock(models.Model):
    ENTRADA = 'entrada'
    SALIDA = 'salida'
    TIPO_CHOICES = [
        (ENTRADA, 'Entrada'),
        (SALIDA, 'Salida'),
    ]

    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='movimientos')
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    cantidad = models.PositiveIntegerField()
    motivo = models.CharField(max_length=200, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tipo.upper()} - {self.producto.nombre} ({self.cantidad})"

    def clean(self):
        if self.tipo == self.SALIDA and self.pk is None:
            if self.cantidad > self.producto.stock_actual:
                raise ValidationError(
                    f"No hay suficiente stock. Stock actual: {self.producto.stock_actual}, "
                    f"intentaste sacar: {self.cantidad}."
                )

    def save(self, *args, **kwargs):
        es_nuevo = self.pk is None
        if es_nuevo:
            self.full_clean()
        super().save(*args, **kwargs)
        if es_nuevo:
            if self.tipo == self.ENTRADA:
                self.producto.stock_actual += self.cantidad
            else:
                self.producto.stock_actual -= self.cantidad
            self.producto.save()