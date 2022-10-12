# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True, unique=True
#   * Make sure each OneToOneField and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from datetime import datetime
from django.forms import model_to_dict

       



       


       
      


class EstadoOrdentrabajo(models.Model):
    idordentrabajo = models.IntegerField(primary_key=True, unique=True)
    estado = models.CharField(max_length=45, blank=True, null=True)
    def __str__(self): #como van a salir en mis vistas
        return self.estado
    class Meta:
        verbose_name = 'EstadoOrdentrabajo'
        verbose_name_plural = 'EstadoOrdentrabajos'
        ordering = ['idordentrabajo']




      

class Material(models.Model):
    idmaterial = models.IntegerField(primary_key=True, unique=True, default=0)
    nombre = models.CharField(max_length=45, blank=True, null=True)
    descripcion = models.CharField(max_length=45, blank=True, null=True)
    stock = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    precio_unidad = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self): #como van a salir en mis vistas
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self)
        item['precio_unidad'] = float(self.precio_unidad)
        item['stock'] = float(self.precio_unidad)
        return item
  

    class Meta:
        verbose_name = 'Material'
        verbose_name_plural = 'Materiales'
        ordering = ['idmaterial']

class Articulo(models.Model):
    fecha = models.DateField(default=datetime.now)
    idarticulo = models.IntegerField(primary_key=True, unique=True) 
    codigo = models.CharField(max_length=45, blank=True, null=True)
    nombre = models.CharField(max_length=45, blank=True, null=True)
    precio = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    descripcion = models.CharField(max_length=45, blank=True, null=True)
    mano_de_obra = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    otrosgastos = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    costo_material = models.FloatField(blank=True, null=True)
    cantidad_material = models.FloatField(blank=True, null=True)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    porciento = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self)
        item['precio'] = float(self.precio)
        item['mano_de_obra'] = float(self.mano_de_obra) 
        item['otrosgastos'] = float(self.otrosgastos)
        item['costo_material'] = float(self.costo_material) 
        item['subtotal'] = float(self.subtotal)
        item['porciento'] = float(self.porciento)
        item['det'] = [i.toJSON() for i in self.detarticulo_set.all()]
        return item

    class Meta:
       verbose_name = 'Articulo'
       verbose_name_plural = 'Articulos'
       ordering = ['idarticulo']


class Detarticulo(models.Model):
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    precio = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cant = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.prod.name

    def toJSON(self):
        item = model_to_dict(self, exclude=['articulo'])
        item['material'] = self.material.toJSON()
        item['precio'] = format(self.price, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        return item

    class Meta:
        verbose_name = 'Detalle articulo'
        verbose_name_plural = 'Detalle articulos'
        ordering = ['id']



       
class Cliente(models.Model):
    nombre = models.CharField(max_length=45, blank=False, null=True, )
    descripcion = models.CharField(max_length=45, blank=True, null=True)
    direccion = models.CharField(max_length=45, blank=True, null=True)
    telefono = models.CharField(max_length=45, blank=True, null=True)
    nit = models.FloatField(max_length=10, blank=True, null=True)  # Field name made lowercase.
    
    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['id']
       
        


class Cotizacion(models.Model):
    terminos = models.CharField(max_length=45, blank=True, null=True)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    porciento = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    fecha = models.DateField(default=datetime.now)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, default=0)
    
    
    def toJSON(self):
        item = model_to_dict(self)
        item['cliente'] = self.cliente.toJSON()
        item['terminos'] = self.cliente.toJSON()
        item['subtotal'] = format(self.subtotal, '.2f')
        item['total'] = format(self.total, '.2f')
        item['porciento'] = format(self.porciento, '.2f')
        item['fecha'] = self.fecha.strftime('%Y-%m-%d')
        item['det'] = [i.toJSON() for i in self.detcotizacion_set.all()]

    class Meta:
        verbose_name = 'Cotizacion'
        verbose_name_plural = 'Cotizaciones'
        ordering = ['id']
       
class Detcotizacion(models.Model):
        
    cotizacion = models.ForeignKey(Cotizacion, on_delete=models.CASCADE)
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)
    precio = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cant = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.prod.name

    def toJSON(self):
        item = model_to_dict(self, exclude=['cotizacion'])
        item['articulo'] = self.articulo.toJSON()
        item['precio'] = format(self.price, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        return item

    class Meta:
        verbose_name = 'Detalle cotizacion'
        verbose_name_plural = 'Detalle cotizaciones'
        ordering = ['id']

class Proveedores(models.Model):
    idproveedores = models.IntegerField(primary_key=True, unique=True)
    nombre = models.CharField(max_length=45, blank=True, null=True)
    direccion = models.CharField(max_length=45, blank=True, null=True)
    telefono = models.IntegerField(blank=True, null=True)
    descripcion = models.CharField(max_length=45, blank=True, null=True)
    def __str__(self):
        return self.nombre

    
    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['idproveedores']

class OrdenCompraMaterial(models.Model):
    idorden_compra_material = models.IntegerField(primary_key=True, unique=True)
    total = models.CharField(max_length=45, blank=True, null=True)
    descripcion = models.CharField(max_length=45, blank=True, null=True)
    observaciones = models.CharField(max_length=45, blank=True, null=True)
    proveedor = models.ForeignKey(Proveedores, on_delete=models.CASCADE, default=0)
    class Meta:
        verbose_name = 'OrdenCompraMaterial'
        verbose_name_plural = 'OrdenCompraMateriales'
        ordering = ['idorden_compra_material']
     



    

class Persona(models.Model):
    idpersona = models.IntegerField(primary_key=True, unique=True)
    nombre = models.CharField(max_length=45, blank=True, null=True)
    apellido = models.CharField(max_length=45, blank=True, null=True)
    direccion = models.CharField(max_length=45, blank=True, null=True)
    telefono = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.nombre
    class Meta:
        verbose_name = 'Persona'
        verbose_name_plural = 'Personas'
        ordering = ['idpersona']


class Puestoempleado(models.Model):
    idpuestoempleado = models.IntegerField(primary_key=True, unique=True)
    nombre = models.CharField(max_length=45, blank=True, null=True)
    descripcion = models.CharField(max_length=45, blank=True, null=True)

    def __str__(self):
        return self.nombre
    class Meta:
        verbose_name = 'Puestoempleado'
        verbose_name_plural = 'Puestoempleados'
        ordering = ['idpuestoempleado']

class Empleado(models.Model):
    idempleado = models.IntegerField(primary_key=True, unique=True)
    persona = models.OneToOneField(Persona,  default=0, on_delete=models.CASCADE, related_name='empleadopersona')
    puestoempleado = models.OneToOneField(Puestoempleado, on_delete=models.CASCADE, default=0, related_name='empleadopuesto')

    def __str__(self):
        return self.persona
    class Meta:
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'
        ordering = ['idempleado']
       


    


     

class Tipoinventario(models.Model):
    idtipoinventario = models.IntegerField(primary_key=True, unique=True)
    tipo = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        verbose_name = 'Tipoinventario'
        verbose_name_plural = 'Tipoinventarios'
        ordering = ['idtipoinventario']

class Inventario(models.Model):
    idinventario = models.IntegerField(primary_key=True, unique=True)
    cantidad = models.IntegerField(blank=True, null=True)
    tipo = models.OneToOneField(Tipoinventario, on_delete=models.CASCADE, default=0, related_name='inventariotipo')
    inventario_material = models.ForeignKey(Material, on_delete=models.CASCADE, default=0, related_name='inventariomaterial')

    class Meta:
        verbose_name = 'Inventario'
        verbose_name_plural = 'Inventarios'
        ordering = ['idinventario']
     
class EstadoVenta(models.Model):
    idestado_venta = models.IntegerField(primary_key=True, unique=True)
    estado = models.CharField(max_length=45, blank=True, null=True)

    def __str__(self):
        return self.estado
    class Meta:
        verbose_name = 'EstadoVenta'
        verbose_name_plural = 'EstadoVentas'
        ordering = ['idestado_venta']
     



class Venta(models.Model):
    idventa = models.IntegerField(primary_key=True, unique=True)
    hora_fecha = models.DateTimeField(blank=True, null=True)
    estado = models.CharField(max_length=45, blank=True, null=True)
    fecha = models.DateField(default=datetime.now, verbose_name='Fecha_venta')
    cotizacion = models.OneToOneField(Cotizacion, on_delete=models.CASCADE, db_column='idcotizacion', default=0, related_name='ventacotizacion')
    cliente = models.OneToOneField(Cotizacion, on_delete=models.CASCADE, db_column='cliente', default=0, related_name='ventaclientecotizacion')
    articulo = models.ForeignKey(Cotizacion, on_delete=models.CASCADE, db_column='articulo', default=0, related_name='ventaarticulocotizacion')
    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        ordering = ['idventa']
             
class Ordendetrabajo(models.Model):
    idordendetrabajo = models.IntegerField(primary_key=True, unique=True)
    definicion = models.CharField(max_length=45, blank=True, null=True)
    fecha_empieza = models.DateField(blank=True, null=True)
    fecha_termina = models.DateField(blank=True, null=True)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE,  default=0)
    estado = models.ForeignKey(EstadoOrdentrabajo, on_delete=models.CASCADE,  default=0)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, default=0)

    def __str__(self):
        return self.prod.name

    def toJSON(self):
        item = model_to_dict(self)
        item['cliente'] = self.cliente.toJSON()
        item['persona'] = self.persona.toJSON()
        item['estado'] = self.estado.toJSON()
        item['definicion'] = self.definicion.toJSON()
        item['subtotal'] = format(self.subtotal, '.2f')
        item['idordendetrabajo'] = format(self.total, '.2f')
        item['fecha_empieza'] = self.fecha.strftime('%Y-%m-%d')
        item['fecha_termina'] = self.fecha.strftime('%Y-%m-%d')
        item['det'] = [i.toJSON() for i in self.detordentrabajo_set.all()]

class Meta:
        verbose_name = 'Ordendetrabajo'
        verbose_name_plural = 'Ordendetrabajos'
        ordering = ['idordendetrabajo']

class Detordentrabajo(models.Model):
        
    idordendetrabajo = models.ForeignKey(Ordendetrabajo, on_delete=models.CASCADE)
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)
    cant = models.IntegerField(default=0)

    def __str__(self):
        return self.prod.name

    def toJSON(self):
        item = model_to_dict(self, exclude=['ordendetrabajo'])
        item['articulo'] = self.articulo.toJSON()
        return item

    class Meta:
        verbose_name = 'Detalle orden de trabajo'
        verbose_name_plural = 'Detalle ordenes de trabajo'
        ordering = ['id']

#class Usuario(models.Model):
class Envios(models.Model):
    idenvios = models.IntegerField(primary_key=True, unique=True)
    fecha = models.DateField(default=datetime.now, verbose_name='Fecha_envio')
    observaciones = models.CharField(db_column='Observaciones', max_length=45, blank=True, null=True)  # Field name made lowercase.
    fecha = models.DateField(default=datetime.now)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, default=0)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE,  default=0)
    class Meta:
        verbose_name = 'Envio'
        verbose_name_plural = 'Envios'
        ordering = ['idenvios']
            

       