from django.forms import *
from datetime import datetime
from django import forms
from .models import Articulo, Cotizacion, Material, Persona, Cliente, Proveedores
#formulario persona
class PersonaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off' #esto es para aplicar formato recorriendo mis fields
            
    class Meta:
        model = Persona
        fields = '__all__'

        widgets = { #me permite personalizar mi componentes de mi from en mi html
            'nombre': TextInput(
                attrs= {
                    'placeholder': 'Ingrese nombre',
                    
                }
            ),
            'apellido': TextInput(
                attrs= {
                    'placeholder': 'Ingrese nombre',
                   
                }
            )
        }

#formulario clientes
class ClienteForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off' #esto es para aplicar formato recorriendo mis fields
            
    class Meta:
        model = Cliente
        fields = '__all__'

        widgets = { #me permite personalizar mi componentes de mi from en mi html
            'nombre': TextInput(
                attrs= {
                    'placeholder': 'Ingrese nombre',
                    
                }
            ),
            
        }

#formulario proveedores
class ProveedoresForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off' #esto es para aplicar formato recorriendo mis fields
            
    class Meta:
        model = Proveedores
        fields = '__all__'

        widgets = { #me permite personalizar mi componentes de mi from en mi html
            'nombre': TextInput(
                attrs= {
                    'placeholder': 'Ingrese nombre',
                    
                }
            ),
            
        }     

#formulario articulo
class ArticuloForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off' #esto es para aplicar formato recorriendo mis fields
            
    class Meta:
        model = Articulo
        fields = '__all__'

        widgets = { #me permite personalizar mi componentes de mi from en mi html
            'nombre': TextInput(
                attrs= {
                    'placeholder': 'Ingrese nombre',
                    
                }
            ),
            
        }        
   
#formulario proveedores
class MaterialForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off' #esto es para aplicar formato recorriendo mis fields
            
    class Meta:
        model = Material
        fields = '__all__'

        widgets = { #me permite personalizar mi componentes de mi from en mi html
            'nombre': TextInput(
                attrs= {
                    'placeholder': 'Ingrese nombre',
                    
                }
            ),
            
        }        
   
#formulario cotizacion

class CotizacionForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off' #esto es para aplicar formato recorriendo mis fields
        
        self.fields['subtotal'].widget.attrs = {
            'readonly': True,
            'class': 'form-control',
            
        }
        self.fields['total'].widget.attrs = {
            'readonly': True,
            'class': 'form-control',
            
        }


    class Meta:
        model = Cotizacion
        fields = '__all__'
        widgets = {
             #me permite personalizar mi componentes de mi form en mi html
             'cliente': forms.Select(attrs={
                'class': 'custom-select select2',
             }),

             'fecha': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'fecha',
                    'data-target': '#fecha',
                    'data-toggle': 'datetimepicker'
        }        
   
             )
        }