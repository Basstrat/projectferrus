from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from AppFerrus.models import Articulo, Material, Cliente
from AppFerrus.forms import ArticuloForm
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect





class articulolistview(ListView):
    model = Articulo
    template_name = 'articulo/lista.html' # este es el que uso para mi listado

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs): 
        return super().dispatch(request, *args, **kwargs)
  







#este es para mi formulario

class articuloCreateView(CreateView):
    model = Articulo #aqui llamo a mi modelo
    form_class = ArticuloForm #aqui llamo a mi form de fomrs.py
    template_name = 'articulo/crearregistro.html' #direccion de la pagina que voy usar
    success_url = reverse_lazy('articulolista') #direccion hacia donde voy a redireccionar
    
    #aqui viy a definir para cuando se aguarde un dato repetido
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs): 
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_material': #la variable de mi form js
                data = [] #esto porque es un array
                materiales = Cliente.objects.filter(nombre__icontains=request.POST['variablebusqueda'])[0:10] #limitante de mostrar
                for i in materiales:
                    item = i.toJSON() #aqui llamo a mi json de mis modelos
                    item['value'] = i.nombre #esto me retornara lo que busco
                    data.append(item) #item es lo que va tirar la busqueda
            
            else:
                data['error'] = 'Ha ocurrido un error 5'
        except Exception as e:
                data['error'] = str(e)
        return JsonResponse(data, safe=False) # para serializarlos cuando es coleccion de elemento ponemos false

    def get_context_data(self, **kwargs): 
        context= super().get_context_data(**kwargs)
        context['title'] = 'Crear una Articulo'
        context['entity'] = 'Articulos' #titulo de la tabla y pestaña
        return context 
        #los decoradores pueden modificar de una forma dinamica una funcion



#vista para eliminar registros
class articuloDeleteView(DeleteView):
    model = Articulo #aqui llamo a mi modelo
    template_name = 'articulo/eliminaregistro.html' #direccion de la pagina que voy usar
    success_url = reverse_lazy('articulolista') #direccion hacia donde voy a redireccionar
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs): 
        return super().dispatch(request, *args, **kwargs)
        
    def get_context_data(self, **kwargs): 
        context= super().get_context_data(**kwargs)
        context['title'] = 'Eliminacion'
        context['crear_url'] =  reverse_lazy('articuloeliminaregistro')
        context['lista_url'] = self.success_url
        return context 