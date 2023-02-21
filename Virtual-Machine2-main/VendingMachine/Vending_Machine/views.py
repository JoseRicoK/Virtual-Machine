from django.shortcuts import render, redirect
from .models import Producto
from django.views import generic

from django.core.exceptions import ObjectDoesNotExist

from django.contrib import messages

def index(request):
    productos = Producto.objects.all()
    context = {'productos': productos}
    return render(request, 'index.html', context)



def pagar(request):
    if request.method == 'POST':
        codigoProducto = request.POST['codigoDeProducto']
        try:
            producto = Producto.objects.get(codigo_producto=codigoProducto)
            productos = Producto.objects.all()
            if producto.stock <= 0:
                return redirect('/')
            producto.stock -= 1
            producto.num_comprados += 1
            producto.save()
            mensaje = f"¡Gracias por comprar {producto.nombre_producto}!"
            return render(request, 'index.html', {'mensaje':mensaje, 'productos': productos})
        except ObjectDoesNotExist:
            return redirect('/')
    else:
        return redirect('/')




class ProductListView(generic.ListView):
    model = Producto

class ProductDetailView(generic.DetailView):
    model = Producto

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['codigo_producto'] = self.object.codigo_producto
        return context

class ProductEditView(generic.UpdateView):
    model = Producto
    template_name_suffix = "_edit"
    fields = ['nombre_producto', 'precio', 'stock', 'num_comprados']

def zonaAdmin(request):
    productos = Producto.objects.all()
    context = {'productos': productos}
    return render(request, 'parteAdmin.html', context=context)

def editPrecio(request):
    productos = Producto.objects.all()
    context = {'productos': productos}
    return render(request, 'edit_precio.html', context=context)


def alertarProveedor(request):
    # Obtiene todos los productos con stock igual o inferior a 1
    productos_bajo_stock = Producto.objects.filter(stock__lte=1)

    # Verifica si se ha enviado un formulario
    if request.method == 'POST':
        # Obtiene el valor del campo de entrada "producto"
        producto_nombre = request.POST['producto']

        # Obtiene el producto con el nombre especificado
        producto = Producto.objects.get(nombre_producto=producto_nombre)

        # Actualiza el stock del producto a 6
        producto.stock = 6
        producto.save()

        # Redirige al usuario a la misma página
        return redirect('alertar-proveedor')

    context = {'productos_bajo_stock': productos_bajo_stock}
    return render(request, 'alertar_proveedor.html', context=context)


def verEstadisticas(request):
    productos = Producto.objects.all().order_by('-num_comprados')

    ingresos = []
    for producto in productos:
        ingreso = producto.num_comprados * producto.precio
        ingresos.append((producto, ingreso))
    productos_ordenados = sorted(ingresos, key=lambda x: x[1], reverse=True)
    producto_mayor_ganancia = productos_ordenados[0][0]

    # Calcula el ingreso total por producto
    for producto in productos:
        producto.ingreso_total = producto.num_comprados * producto.precio

    # Calcula el ingreso total de todos los productos
    ingreso_total = sum(producto.ingreso_total for producto in productos)

    context = {'productos': productos, 'ingreso_total': ingreso_total, 'producto_mayor_ganancia': producto_mayor_ganancia}
    return render(request, 'ver_estadisticas.html', context=context)




