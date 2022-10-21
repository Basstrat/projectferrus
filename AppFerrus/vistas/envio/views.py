from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from AppFerrus.models import Cotizacion, Envios, Detenvios
from AppFerrus.forms import CotizacionForm, EnviosForm
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
import json
from django.db import transaction

from AppFerrus.models import Articulo
from AppFerrus.models import Detcotizacion

from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string


#from weasyprint.fonts import FontConfiguration

#librerias para pdf
import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders


    #vista basada en clases

class Envioslistview(ListView):
    model = Envios
    template_name = 'envio/lista.html' # este es el que uso para mi listado

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = [] #es una array
                for i in Envios.objects.all():
                    data.append(i.toJSON()) #incrustar datos dentro del array
             
            elif action == 'search_details_prod':
                data = []
                for i in Detenvios.objects.filter(cotizacion_id=request.POST['id']):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False) #safe= false para que maneje varios datos

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado Envios'
        context['entity'] = 'Envios'
        context['create_url'] = reverse_lazy('cotizacioncrear')
        context['list_url'] = reverse_lazy('cotizacionlistado')
        return context





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
                articulos = Articulo.objects.filter(nombre__icontains=request.POST['variablebusqueda'], stock__gt=0)[0:10] #limitante de mostrar
                for i in articulos:
                    item = i.toJSON() #aqui llamo a mi json de mis modelos
                    item['value'] = i.nombre #esto me retornara lo que busco
                    data.append(item) #item es lo que va tirar la busquedao que va tirar la busqueda

            elif action == 'add': #para añadir mi registro
                print(request.POST)
                products = json.loads(request.POST['products'])
                envio = Envios()
                envio.fecha = request.POST['fecha']
                envio.cliente_id = request.POST['cliente']
                envio.observaciones = request.POST['observaciones']
                envio.persona_id = request.POST['persona']
                envio.idenvios = request.POST['idenvios']
                envio.save()
                
                
    #iterar productos
                for i in products:
                    det = Detenvios()
                    det.idenvios = envio
                    det.articulo_id = i['idarticulo']
                    det.cant = int(i['cant'])
                    det.save()
                    det.articulo.stockenviado+=det.cant
                    det.articulo.stock-=det.cant
                    det.articulo.save()
                
                    
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
                data['error'] = str(e)
        return JsonResponse(data, safe=False) # para serializarlos cuando es coleccion de elemento ponemos false

    def get_context_data(self, **kwargs): 
        context= super().get_context_data(**kwargs)
        context['title'] = 'Crear envio'
        context['entity'] = 'orden de trabajo' #titulo de la tabla y pestaña
        context['action'] = 'add'
        return context 
        #los decoradores pueden modificar de una forma dinamica una funcion



class envioPdfView(View):
    def link_callback(uri, rel): #para llamar archivos estaticos
            """
            Convert HTML URIs to absolute system paths so xhtml2pdf can access those
            resources
            """
            result = finders.find(uri)
            if result:
                    if not isinstance(result, (list, tuple)):
                            result = [result]
                    result = list(os.path.realpath(path) for path in result)
                    path=result[0]
            else:
                    sUrl = settings.STATIC_URL        # Typically /static/
                    sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
                    mUrl = settings.MEDIA_URL         # Typically /media/
                    mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

                    if uri.startswith(mUrl):
                            path = os.path.join(mRoot, uri.replace(mUrl, ""))
                    elif uri.startswith(sUrl):
                            path = os.path.join(sRoot, uri.replace(sUrl, ""))
                    else:
                            return uri

            # make sure that file exists
            if not os.path.isfile(path):
                    raise Exception(
                            'media URI must start with %s or %s' % (sUrl, mUrl)
                    )
            return path
    
    
    
    
    
    def get(self, request, *args, **kwargs):
        try:
            template = get_template('envio/pdf.html') #aqui obtiene la ruta de la plantilla
            context = {'envio': Envios.objects.get(pk=self.kwargs['pk']),
            'comp':{'nombre': 'Multiservicios Agroindustriales Ferrus', 'direccion':'San Jose Pinula Km. 20'},
            } # mi diccionario
            html = template.render(context) #rerenderizar mi diccinario
            response = HttpResponse(content_type='application/pdf')
            #response['Content-Disposition'] = 'attachment; filename="report.pdf"' # mi respuesta para descargar
            pisaStatus = pisa.CreatePDF( #funcion para crear pdf
            html, dest=response, #objeto que va tener el response
            link_callback=self.link_callback
            )
            return response
        except: 
            pass
        return HttpResponseRedirect(reverse_lazy('personalista')) #en caso de erro me retorna a esta pagina

