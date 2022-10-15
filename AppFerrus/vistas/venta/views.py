from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from AppFerrus.models import Cotizacion, Venta, Detventa
from AppFerrus.forms import CotizacionForm, VentaForm
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
import json

from AppFerrus.models import Articulo
from AppFerrus.models import Detcotizacion





    #vista basada en clases
class Ventalistview(ListView):
    model = Cotizacion
    template_name = 'cotizacion/listpersona.html' # este es el que uso para mi listado

  
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs): 
        return super().dispatch(request, *args, **kwargs)






#este es para mi formulario

class VentaCreateView(CreateView):
    model = Venta #aqui llamo a mi modelo
    form_class = VentaForm #aqui llamo a mi form de fomrs.py
    template_name = 'Venta/crearregistro.html' #direccion de la pagina que voy usar
    success_url = reverse_lazy('cotizacionlista') #direccion hacia donde voy a redireccionar
    
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
                articulos = Articulo.objects.filter(stock__gt=0) #unicamnete llamar articulo mayor a cero
                for i in articulos:
                    item = i.toJSON() #aqui llamo a mi json de mis modelos
                    item['value'] = i.nombre #esto me retornara lo que busco
                    data.append(item) #item es lo que va tirar la busqueda

            elif action == 'add': #para añadir mi registro
                print(request.POST)
                cotizacion1 = json.loads(request.POST['cotizacion1'])
                venta = Venta()
                venta.fecha = cotizacion1['fecha']
                venta.cliente_id = cotizacion1['cliente']
                venta.subtotal = float(cotizacion1['subtotal'])
                venta.total = float(cotizacion1['total'])
                venta.idventa = cotizacion1['idventa']
                venta.estado_id = cotizacion1['estado']
                venta.save()
    #iterar productos
                for i in cotizacion1['articulo']:
                    det = Detventa()
                    det.venta_id = venta.idventa
                    det.articulo = i['articulo']
                    det.cant = int(i['cant'])
                    det.precio = float(i['precio'])
                    det.subtotal = float(i['subtotal'])
                    det.save()
                    det.articulo.stock-=det.cant
                    det.articulo.save()
            
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
                data['error'] = str(e)
        return JsonResponse(data, safe=False) # para serializarlos cuando es coleccion de elemento ponemos false


    def get_context_data(self, **kwargs): 
        context= super().get_context_data(**kwargs)
        context['title'] = 'Crear una Cotizacion'
        context['entity'] = 'Cotizaciones' #titulo de la tabla y pestaña
        return context 
        #los decoradores pueden modificar de una forma dinamica una funcion



