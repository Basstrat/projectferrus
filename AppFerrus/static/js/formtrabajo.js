var tblarticulos;
var cotizacion1 = {
    items:  {
        idordendetrabajo: 0.00,
        definicion: '',
        cliente: '',
        fecha_empieza: '',
        fecha_termina: '',
        articulo: [],
    },
    
    calcularcotizacion1: function() {


    },
    
    list: function () {
        this.calcularcotizacion1();
        tblarticulos= $('#tblarticulo').DataTable( { //aqui asigno mi variable table
            responsive: true,
            autoWidth: false,
            destroy: true,
            data: this.items.articulo,
            columns: [
                {"data": "idarticulo" },
                {"data": "nombre"},
                {"data": "descripcion"},
   
      
            ],
            columnDefs: [
                {
                targets: [0],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row){
                    return '<a rel="remove" class="btn btn-danger btn-sm">Eliminar</a>';
            }, 
        },
    
            
    
    {
        targets: [3],
        class: 'text-center',
        orderable: false,
        render: function (data, type, row){
            return '<input type="text" name="cant" class="form-control form-control-sm" autocomplete="off"> ';
    },
    },
    
    
    ],

    //a medida que se vaya creado un nuevo registro se pueden ir modificando cierto datos
    rowCallback(row, data, displayNum, displayIndex, dataIndex){ 
        //row contien mis campos, y data la informacion
        $(row).find('input[name="cant"]').TouchSpin({
            min: 1,
            max: 1000,
            step: 1
        })
        .val(1);
    },
    initComplete: function(settings, json){
    
    }
        });
    
    },};




$(function() {
    $('.select2').select2( {
        theme: "bootstrap4",
        language: 'es'
    });

    $('#fecha').datetimepicker({ /*este es el formato de mi fecha*/ 
        format: 'YYYY-MM-DD',
        date: moment().format("YYYY-MM-DD"),
    
    
        
});




//busqueda de productos
$('input[name="buscar"]').autocomplete({ //nombre de mi barra de busqueda
    source: function (request, response) {
        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'search_articulo', //llamar esta en mi vista action POST
                'variablebusqueda': request.term
            },
            dataType: 'json',
        }).done(function (data) {
            response(data);
        }).fail(function (jqXHR, textStatus, errorThrown) {
            //alert(textStatus + ': ' + errorThrown);
        }).always(function (data) {

        });
    },
    delay: 500,
    minLength: 1,
    select: function (event, ui) {
        event.preventDefault();
        //item es la variable que viene del form
        //ui.item.cantidad = cant;
        ui.item.subtotal = 0.00;
        cotizacion1.items.articulo.push(ui.item); //para agregar mi items a mi estrucutra de variable cotizacion1
        console.log(cotizacion1.items);
        cotizacion1.list();//para que se enlisten los items
        $(this).val('');

    }
});



//evento cantidad articulos  //al cambio y que se actulizce
$('#tblarticulo tbody')
.on('click','[rel=remove]', function(){ //cuando haga click en el boton eliminar
    var tr = tblarticulos.cell($(this).closest('td, li')).index(); //llamo a mi tabla
    cotizacion1.items.articulo.splice(tr.row, 1); //esta es mi posicion actual
    cotizacion1.list();
})


//cuando guarde mi post
$('form').on('submit', function (e){
    e.preventDefault();
    cotizacion1.items.idordendetrabajo = $('input[name="idordendetrabajo"]').val();
    cotizacion1.items.fecha_empieza = $('input[name="fecha_empieza"]').val();
    cotizacion1.items.fecha_termina = $('input[name="fecha_termina"]').val(); //aqui llamo a los valores de mis inputs html
    cotizacion1.items.cliente = $('select[name="cliente"]').val();
    cotizacion1.items.estado = $('input[name="estado"]').val();
    cotizacion1.items.definicion = $('input[name="definicion"]').val();
    var parameters = new FormData();

    parameters.append('action', $('input[name="action"]').val()); //aqui mando los parametros dek html con append
    parameters.append('cotizacion1', JSON.stringify(cotizacion1.items)); //para convertir json a string
    submit_with_ajax(window.location.pathname, 'Notificacion', 'Desea guardar?', parameters, function (){
        location.href =  '/erp/cotizacion/listado/';
    })


})
});




