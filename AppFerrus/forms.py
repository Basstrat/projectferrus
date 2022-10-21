from django.forms import *
from datetime import datetime
from django import forms
from .models import Articulo, Cotizacion, Empleado, Envios, Material, OrdenCompraMaterial, Ordendetrabajo, Persona, Cliente, Proveedores, Venta, Usuario


class FormularioUsuario(forms.ModelForm):
    """ Formulario de Registro de un Usuario en la base de datos
    Variables:
        - password1:    Contraseña
        - password2:    Verificación de la contraseña
    """
    password1 = forms.CharField(label = 'Contraseña',widget = forms.PasswordInput(
        attrs = {
            'class': 'form-control',
            'placeholder': 'Ingrese su contraseña...',
            'id': 'password1',
            'required':'required',
        }
    ))

    password2 = forms.CharField(label = 'Contraseña de Confirmación', widget = forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese nuevamente su contraseña...',
            'id': 'password2',
            'required': 'required',
        }
    ))

    class Meta:
        model = Usuario
        fields = ('username','nombres')
        widgets = {
           
            'nombres': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese su nombre',
                }
            ),
            
            'username': forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Ingrese su nombre de usuario',
                }
            ),
           
        }

    def clean_password2(self):
        """ Validación de Contraseña
        Metodo que valida que ambas contraseñas ingresadas sean igual, esto antes de ser encriptadas
        y guardadas en la base dedatos, Retornar la contraseña Válida.
        Excepciones:
        - ValidationError -- cuando las contraseñas no son iguales muestra un mensaje de error
        """
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError('Contraseñas no coinciden!')
        return password2

    def save(self,commit = True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user






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
            
            
            self.fields['precio'].widget.attrs = {
            'readonly': False,
            'class': 'form-control',
            
        }
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
   
             ),
              'porciento': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'subtotal': forms.TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
            'total': forms.TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            })
        }


class ordendetrabajoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off' #esto es para aplicar formato recorriendo mis fields
            
    class Meta:
        model = Ordendetrabajo
        fields = '__all__'

        widgets = { #me permite personalizar mi componentes de mi from en mi html
            'nombre': TextInput(
                attrs= {
                    'placeholder': 'Ingrese nombre',
                    
                }
            ),
             'fecha': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'fecha_empieza',
                    'data-target': '#fecha',
                    'data-toggle': 'datetimepicker'
        }        
   
             ),
               
   
            
        }  

#formulario empleado
class EmpleadoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off' #esto es para aplicar formato recorriendo mis fields
            
    class Meta:
        model = Empleado
        fields = '__all__'


#formulario envio
class EnviosForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off' #esto es para aplicar formato recorriendo mis fields
            
    class Meta:
        model = Envios
        fields = '__all__'
    


#formulario enviu
class VentaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off' #esto es para aplicar formato recorriendo mis fields
            
    class Meta:
        model = Venta
        fields = '__all__'


    

#formulario orden de compra
class OrdendecompraForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off' #esto es para aplicar formato recorriendo mis fields
            
    class Meta:
        model = OrdenCompraMaterial
        fields = '__all__'
    widgets = {
            'articulo': forms.Select(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
            
        }