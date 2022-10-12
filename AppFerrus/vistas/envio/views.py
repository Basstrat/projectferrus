from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from AppFerrus.models import Ordendetrabajo, Cotizacion, Articulo, Envios
from AppFerrus.forms import ordendetrabajoForm, EnviosForm
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
import json

from AppFerrus.models import Articulo






    #vista basada en clases
class Envioslistview(ListView):
    model = Ordendetrabajo
    template_name = 'envio/lista.html' # este es el que uso para mi listado

  

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs): 
        return super().dispatch(request, *args, **kwargs)





#este es para mi formulario

class EnviosCreateView(CreateView):
    model = Envios #aqui llamo a mi modelo
    form_class = EnviosForm #aqui llamo a mi form de fomrs.py
    template_name = 'envio/crearregistro.html' #direccion de la pagina que voy usar
    success_url = reverse_lazy('enviolista') #direccion hacia donde voy a redireccionar
    @method_decorator(csrf_exempt) 
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    #aqui viy a definir para cuando se aguarde un dato repetido
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            print(request.POST)
            if action == 'search_articulo': #la variable de mi form js
                data = [] #esto porque es un array
                articulos = Articulo.objects.filter(nombre__icontains=request.POST['variablebusqueda'])[0:10] #limitante de mostrar
                for i in articulos:
                    print(i.nombre)
                    item = i.toJSON() #aqui llamo a mi json de mis modelos
                    item['value'] = i.nombre #esto me retornara lo que busco
                    data.append(item) #item es lo que va tirar la busqueda

            elif action == 'add': #para añadir mi registro
                print(request.POST)
                cotizacion1 = json.loads(request.POST['cotizacion1'])
                cotizacion = Cotizacion()
                cotizacion.fecha = cotizacion1['fecha']
                cotizacion.cliente_id = cotizacion1['cliente']
                cotizacion.subtotal = float(cotizacion1['subtotal'])
                cotizacion.total = float(cotizacion1['total'])
                cotizacion.porciento = float(cotizacion1['porciento'])
                cotizacion.terminos = cotizacion1['terminos']
                cotizacion.save()
                
    #iterar productos
                for i in cotizacion1['articulo']:
                    det = Detcotizacion()
                    det.cotizacion_id = cotizacion.id
                    det.articulo_id = i['idarticulo']
                    det.cant = int(i['cant'])
                    det.precio = float(i['precio'])
                    det.subtotal = float(i['subtotal'])
                    det.save()
                
                    
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
                data['error'] = str(e)
        return JsonResponse(data, safe=False) # para serializarlos cuando es coleccion de elemento ponemos false

    def get_context_data(self, **kwargs): 
        context= super().get_context_data(**kwargs)
        context['title'] = 'Crear envio'
        context['entity'] = 'orden de trabajo' #titulo de la tabla y pestaña
        return context 
        #los decoradores pueden modificar de una forma dinamica una funcion



