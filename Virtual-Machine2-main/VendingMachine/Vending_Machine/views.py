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
            #producto = listaProducto[0]
            print(f" {codigoProducto}")
            print(f"{producto.stock}")
            producto.stock -= 1
            print(f"{producto.stock}")
            producto.num_comprados += 1
            producto.save()
            
        
            
            return redirect('/')
        except ObjectDoesNotExist:
            context = {'error': f"El producto con código {codigoProducto} no existe."}
            return render(request, 'parteAdmin.html', context)
    else:
        context = {'error': "error"}
        return render(request, 'parteAdmin.html', context)



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
    fields = ['codigo_producto', 'nombre_producto', 'precio', 'stock', 'num_comprados']

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




