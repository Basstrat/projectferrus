import re
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from AppFerrus.models import OrdenCompraMaterial, Cotizacion, Detcotizacion, DetOrdenCompra
from AppFerrus.forms import CotizacionForm, OrdendecompraForm
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
import json

from AppFerrus.models import Articulo
from AppFerrus.models import Material






    #vista basada en clases
class orden_compralistview(ListView):
    model = OrdenCompraMaterial
    template_name = 'orden_compra/lista.html' # este es el que uso para mi listado

  
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs): 
        return super().dispatch(request, *args, **kwargs)






#este es para mi formulario

class orden_compraCreateView(CreateView):
    model = OrdenCompraMaterial #aqui llamo a mi modelo
    form_class = OrdendecompraForm #aqui llamo a mi form de fomrs.py
    template_name = 'orden_compra/crearregistro.html' #direccion de la pagina que voy usar
    success_url = reverse_lazy('cotizacionlistado') #direccion hacia donde voy a redireccionar
    
    #aqui viy a definir para cuando se aguarde un dato repetido
    @method_decorator(csrf_exempt) 
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_articulo': #la variable de mi form js
                data = [] #esto porque es un array
                articulos = Articulo.objects.filter(nombre__icontains=request.POST['variablebusqueda'])[0:10] #limitante de mostrar
                for i in articulos:
                    print(i.nombre)
                    item = i.toJSON() #aqui llamo a mi json de mis modelos
                    item['value'] = i.nombre #esto me retornara lo que busco
                    item['cant'] = 1
                    data.append(item) #item es lo que va tirar la busqueda
            elif action == 'add': #para añadir mi registro
                print(request.POST)
                products = json.loads(request.POST['products'])
                ordencompra = OrdenCompraMaterial()
                ordencompra.fecha = request.POST['fecha']
                ordencompra.proveedor_id = request.POST['proveedor']
                ordencompra.subtotal = float(request.POST['subtotal'])
                ordencompra.total = float(request.POST['total'])
                ordencompra.terminos = request.POST['observaciones']
                ordencompra.idorden_compra_material = request.POST['idorden_compra_material']
                ordencompra.save()
                for i in products:
                    det = DetOrdenCompra()
                    det.idorden_compra_material = ordencompra
                    det.articulo_id = i['idarticulo']
                    det.cant = int(i['cant'])
                    det.precio = float(i['precio'])
                    det.subtotal = float(i['subtotal'])
                    det.save()
                    det.articulo.stock+=det.cant
                    det.articulo.save()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
                data['error'] = str(e)
        return JsonResponse(data, safe=False) # para serializarlos cuando es coleccion de elemento ponemos false

    def get_context_data(self, **kwargs): 
        context= super().get_context_data(**kwargs)
        context['title'] = 'Crear una orden de compra'
        context['entity'] = 'Orden de compras' #titulo de la tabla y pestaña
        context['action'] = 'add'
        return context 
        #los decoradores pueden modificar de una forma dinamica una funcion



