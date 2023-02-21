from django.db import models
from django.urls import reverse

class Producto(models.Model):
    codigo_producto = models.IntegerField()
    nombre_producto = models.CharField(max_length=20, default="nombre_producto")
    precio = models.FloatField()
    stock = models.IntegerField(default=6)
    num_comprados = models.IntegerField()

    def get_edit_url(self):
        return reverse('producto-edit', args=[str(self.id)])

    def get_absolute_url(self):
        return reverse('producto-detail', args=[str(self.id)])
    



