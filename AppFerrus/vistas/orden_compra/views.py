import re
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from AppFerrus.models import Detarticulo, OrdenCompraMaterial, Cotizacion, Detcotizacion, DetOrdenCompra
from AppFerrus.forms import CotizacionForm, OrdendecompraForm
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
import json

from AppFerrus.models import Articulo
from AppFerrus.models import Material


#librerias para pdf
import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders


class orden_compralistview(ListView):
    model = OrdenCompraMaterial
    template_name = 'orden_compra/lista.html' # este es el que uso para mi listado

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = [] #es una array
                for i in OrdenCompraMaterial.objects.all():
                    data.append(i.toJSON()) #incrustar datos dentro del array
            elif action == 'search_details_prod':
                data = []
                for i in DetOrdenCompra.objects.filter(cotizacion_id=request.POST['id']):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False) #safe= false para que maneje varios datos


    def get_articulo_detalles(self): #para llamar mis productos
        data = [] #lo hago diccionario
        try:
            for i in DetOrdenCompra.objects.filter(articulo_id=self.get_object().id):
                item = i.articulo.toJSON() #aqui pido mis articulos
                item['cant'] = i.cant #aqui pido mi cantidad
                data.append(item) #aqui llamo al diccionario
        except: 
            pass
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado compra material'
        context['entity'] = 'Compra material'
        context['create_url'] = reverse_lazy('cotizacioncrear')
        context['list_url'] = reverse_lazy('cotizacionlistado')
        return context





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
                articulos = Material.objects.filter(nombre__icontains=request.POST['variablebusqueda'])[0:10] #limitante de mostrar
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
                ordencompra.articulo_id = self.kwargs['pk']
                ordencompra.idorden_compra_material = request.POST['idorden_compra_material']
                ordencompra.save()
                for i in products:
                    det = DetOrdenCompra()
                    det.idorden_compra_material = ordencompra
                    det.material_id = i['idmaterial']
                    det.cant = (i['cant'])
                    det.precio = float(i['precio_unidad'])
                    det.subtotal = float(i['subtotal'])
                    det.save()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
                data['error'] = str(e)
        return JsonResponse(data, safe=False) # para serializarlos cuando es coleccion de elemento ponemos false

    def get_articulo_detalles(self): #para llamar mis productos
        data = [] #lo hago diccionario
        try:
            #for i in Detarticulo.objects.filter(articulo_id=self.get_object().idarticulo):
            for i in Detarticulo.objects.filter(articulo_id=self.kwargs['pk']):
                item = i.material.toJSON() #aqui pido mis articulos
                item['cant'] = i.cant #aqui pido mi cantidad
                data.append(item) #aqui llamo al diccionario
        except: 
            pass
        return data
        
    def get_context_data(self, **kwargs): 
        context= super().get_context_data(**kwargs)
        context['title'] = 'Crear una orden de compra'
        context['entity'] = 'Orden de compras' #titulo de la tabla y pestaña
        context['action'] = 'add'
        context['det'] = json.dumps(self.get_articulo_detalles(), default=str) # para convetir string
        return context 
        #los decoradores pueden modificar de una forma dinamica una funcion



class ordencompraPdfView(View):
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
            template = get_template('orden_compra/pdf.html') #aqui obtiene la ruta de la plantilla
            context = {'ordencompra': OrdenCompraMaterial.objects.get(pk=self.kwargs['pk']),
            'comp':{'nombre': 'Multiservicios Agroindustriales Ferrus', 'direccion':'San Jose Pinula Km. 20'}
            } # mi diccionario
            html = template.render(context) #rerenderizar mi diccionario
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

