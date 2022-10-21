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


class Ventalistview(ListView):
    model = Venta
    template_name = 'venta/lista.html' # este es el que uso para mi listado

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = [] #es una array
                for i in Venta.objects.all():
                    data.append(i.toJSON()) #incrustar datos dentro del array
                 
            elif action == 'search_details_prod':
                data = []
                for i in Detcotizacion.objects.filter(idventa_id=request.POST['id']):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False) #safe= false para que maneje varios datos

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado Venta'
        context['entity'] = 'Venta'
        context['create_url'] = reverse_lazy('cotizacioncrear')
        context['list_url'] = reverse_lazy('cotizacionlistado')
        return context







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
                articulos = Articulo.objects.filter(nombre__icontains=request.POST['variablebusqueda'], stockenviado__gt=0)[0:10] #limitante de mostrar
                for i in articulos:
                    item = i.toJSON() #aqui llamo a mi json de mis modelos
                    item['value'] = i.nombre #esto me retornara lo que busco
                    data.append(item) #item es lo que va tirar la busqueda

            elif action == 'add': #para añadir mi registro
                print(request.POST)
                products = json.loads(request.POST['products'])
                venta = Venta()
                venta.fecha = request.POST['fecha']
                venta.cliente_id = request.POST['cliente']
                venta.subtotal = float(request.POST['subtotal'])
                venta.total = float(request.POST['total'])
                venta.idventa = request.POST['idventa']
                venta.estado_id = request.POST['estado']
                venta.save()
    #iterar productos
                for i in products:
                    det = Detventa()
                    det.idventa = venta
                    det.articulo_id = i['idarticulo']
                    det.cant = int(i['cant'])
                    det.precio = float(i['precio'])
                    det.subtotal = float(i['subtotal'])
                    det.save()
                    det.articulo.stockenviado-=det.cant
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
        context['action'] = 'add'
        return context 
        #los decoradores pueden modificar de una forma dinamica una funcion



