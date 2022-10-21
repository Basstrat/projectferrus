from django.urls import path




#from .views import myfirstbiew, mysecondview
from .vistas.persona.views import Personalistview, PersonaCreateView, PersonaUpdateView, PersonaDeleteView
from .vistas.cliente.views import Clientelistview, ClienteCreateView, ClienteUpdateView, ClienteDeleteView
from .vistas.proveedor.views import Proveedoreslistview, ProveedoresCreateView, ProveedoresUpdateView, ProveedoresDeleteView

from .vistas.articulo.views import articulolistview, articuloCreateView, articuloDeleteView, articuloUpdateView
from .vistas.material.views import materiallistview, materialCreateView, materialUpdateView, materialDeleteView
from .vistas.cotizacion.views import CotizacionCreateView, Cotizacionlistview, cotizacionDeleteView, cotizacionPdfView, cotizacionUpdateView
from .vistas.orden_compra.views import orden_compraCreateView, orden_compralistview, ordencompraPdfView
from .vistas.orden_trabajo.views import orden_trabajoCreateView, orden_trabajolistview, ordentrabajoPdfView
from .vistas.venta.views import VentaCreateView, Ventalistview
from .vistas.envio.views import EnviosCreateView, Envioslistview, envioPdfView
from .vistas.usuario.views import UsuarioCreateView, UsuarioDeleteView, Usuariolistview, UsuarioUpdateView



urlpatterns = [
    #path('uno/', myfirstbiew, name='vista1'),
    #path('segunda/', mysecondview),
    #persona
    path('persona/listado/', Personalistview.as_view(), name = 'personalista' ),
    path('persona/añadirregistro/', PersonaCreateView.as_view(), name = 'personaañadirregistro' ),
    path('persona/editarregistro/<int:pk>/', PersonaUpdateView.as_view(), name = 'personaeditarregistro' ), #int pk para reconosca que id vamos a editar
    path('persona/eliminaregistro/<int:pk>/', PersonaDeleteView.as_view(), name = 'eliminaregistro' ),
    #cliente
    path('cliente/listado/', Clientelistview.as_view(), name = 'clientelista' ),
    path('cliente/añadirregistro/', ClienteCreateView.as_view(), name = 'clienteañadirregistro' ),
    path('cliente/editarregistro/<int:pk>/', ClienteUpdateView.as_view(), name = 'clienteeditarregistro' ), #int pk para reconosca que id vamos a editar
    path('cliente/eliminaregistro/<int:pk>/', ClienteDeleteView.as_view(), name = 'clienteeliminaregistro' ),

    #proveedores
    path('proveedor/listado/',  Proveedoreslistview.as_view(), name = 'proveedoreslista' ),
    path('proveedor/añadirregistro/',  ProveedoresCreateView.as_view(), name = 'proveedoresañadirregistro' ),
    path('proveedor/editarregistro/<int:pk>/',  ProveedoresUpdateView.as_view(), name = 'proveedoreseditarregistro' ), #int pk para reconosca que id vamos a editar
    path('proveedor/eliminaregistro/<int:pk>/',  ProveedoresDeleteView.as_view(), name = 'proveedoreseliminaregistro' ),

  #articulo
    path('articulo/listado/',  articulolistview.as_view(), name = 'articulolista' ),
    path('articulo/añadirregistro/',  articuloCreateView.as_view(), name = 'articuloañadirregistro' ),
    path('articulo/eliminaregistro/<int:pk>/',  articuloDeleteView.as_view(), name = 'articuloeliminaregistro' ),
    path('articulo/editarregistro/<int:pk>/',  articuloUpdateView.as_view(), name = 'articuloeditar' ),


  #material
    path('material/listado/', materiallistview.as_view(), name = 'materiallista' ),
    path('material/añadirregistro/',  materialCreateView.as_view(), name = 'materialañadirregistro' ),
    path('material/editarregistro/<int:pk>/',  materialUpdateView.as_view(), name = 'materialeditarregistro' ), #int pk para reconosca que id vamos a editar
    path('material/eliminaregistro/<int:pk>/',  materialDeleteView.as_view(), name = 'materialeliminaregistro' ),
 
 #cotizacion
    path('cotizacion/crear/', CotizacionCreateView.as_view(), name = 'cotizacioncrear' ),
    path('cotizacion/listado/', Cotizacionlistview.as_view(), name = 'cotizacionlistado' ),
    path('cotizacion/eliminar/<int:pk>/', cotizacionDeleteView.as_view(), name = 'cotizacioneliminar' ),
    path('cotizacion/editar/<int:pk>/', cotizacionUpdateView.as_view(), name = 'cotizacioneditar' ),
    path('cotizacion/imprimir/<int:pk>/', cotizacionPdfView.as_view(), name = 'cotizacionpdf' ),

    path('orden_compra/crear/<int:pk>/', orden_compraCreateView.as_view(), name = 'ordencompracrear' ),
    path('orden_compra/listado/', orden_compralistview.as_view(), name = 'ordencompralistado' ),
    path('orden_compra/imprimir/<int:pk>/', ordencompraPdfView.as_view(), name = 'ordencomprapdf' ),
    
    
    path('orden_trabajo/crear/', orden_trabajoCreateView.as_view(), name = 'ordentrabajocrear' ),
    path('orden_trabajo/listado/', orden_trabajolistview.as_view(), name = 'ordentrabajolistado' ),
    path('orden_trabajo/eliminar/<int:pk>/', cotizacionDeleteView.as_view(), name = 'cotizacioneliminar' ),
    path('orden_trabajo/imprimir/<int:pk>/', ordentrabajoPdfView.as_view(), name = 'ordentrabajopdf' ),

    path('venta/crear/', VentaCreateView.as_view(), name = 'ventacrear' ),
    path('venta/listado/', Ventalistview.as_view(), name = 'ventalistado' ),
   
   #persona
    path('persona/listado/', Personalistview.as_view(), name = 'personalista' ),
    path('persona/añadirregistro/', PersonaCreateView.as_view(), name = 'personaañadirregistro' ),
    path('persona/editarregistro/<int:pk>/', PersonaUpdateView.as_view(), name = 'personaeditarregistro' ), #int pk para reconosca que id vamos a editar
    path('persona/eliminaregistro/<int:pk>/', PersonaDeleteView.as_view(), name = 'eliminaregistro' ),


    #envios
    path('envio/crear/', EnviosCreateView.as_view(), name = 'enviocrear' ),
    path('envio/listado/', Envioslistview.as_view(), name = 'enviolistado' ),
    path('envio/imprimir/<int:pk>/', envioPdfView.as_view(), name = 'enviopdf' ),

   #envios
    path('usuario/listado/', Usuariolistview.as_view(), name = 'usuariolista' ),
    path('usuario/añadirregistro/', UsuarioCreateView.as_view(), name = 'usuarioañadirregistro' ),
    path('usuario/editarregistro/<int:pk>/', UsuarioUpdateView.as_view(), name = 'usuarioeditarregistro' ), #int pk para reconosca que id vamos a editar
    path('usuario/eliminaregistro/<int:pk>/', UsuarioDeleteView.as_view(), name = 'eliminaregistro' ),
]
