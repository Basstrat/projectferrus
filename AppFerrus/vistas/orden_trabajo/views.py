from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from AppFerrus.models import Ordendetrabajo, Cotizacion, Articulo
from AppFerrus.forms import ordendetrabajoForm
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
import json

from AppFerrus.models import Articulo
from AppFerrus.models import Detordentrabajo







    #vista basada en clases
class orden_trabajolistview(ListView):
    model = Ordendetrabajo
    template_name = 'orden_trabajo/lista.html' # este es el que uso para mi listado

  

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs): 
        return super().dispatch(request, *args, **kwargs)





#este es para mi formulario

class orden_trabajoCreateView(CreateView):
    model = Ordendetrabajo #aqui llamo a mi modelo
    form_class = ordendetrabajoForm #aqui llamo a mi form de fomrs.py
    template_name = 'orden_trabajo/crearregistro.html' #direccion de la pagina que voy usar
    success_url = reverse_lazy('orden_trabajolista') #direccion hacia donde voy a redireccionar
    @method_decorator(csrf_exempt) 
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    #aqui viy a definir para cuando se aguarde un dato repetido

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
                    item['cant'] = 1
                    data.append(item) #item es lo que va tirar la busqueda
            elif action == 'add': #para añadir mi registro
                print(request.POST)
                products = json.loads(request.POST['products'])
                ordentrabajo = Ordendetrabajo()
                ordentrabajo.fecha = request.POST['fecha']
                ordentrabajo.estado_id = request.POST['estado']
                ordentrabajo.cliente_id = request.POST['cliente']
                ordentrabajo.persona_idpersona = (request.POST['persona'])
                ordentrabajo.definicion = request.POST['definicion']
                ordentrabajo.idordendetrabajo = request.POST['idordendetrabajo']
                ordentrabajo.save()
                for i in products:
                    det = Detordentrabajo()
                    det.idordendetrabajo = ordentrabajo
                    det.articulo_id = i['idarticulo']
                    det.cant = int(i['cant'])
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
        context['title'] = 'Crear una orden de trabajo'
        context['entity'] = 'orden de trabajo' #titulo de la tabla y pestaña
        return context 
        #los decoradores pueden modificar de una forma dinamica una funcion



