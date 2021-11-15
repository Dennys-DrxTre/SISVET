
var tblCate;
var modal_title;
var messages;

/** TABLE PRODUCT */
function getData() {
    tblCate = $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        "language": {
            "sProcessing": "Procesando...",
            "sLengthMenu": "Mostrar _MENU_ registros",
            "sZeroRecords": "No se encontraron resultados",
            "sEmptyTable": "Ningún dato disponible en esta tabla",
            "sInfo": "Mostrando del _START_ al _END_ de un total de _TOTAL_ registros",
            "sInfoEmpty": "Mostrand del 0 al 0 de un total de 0 registros",
            "sInfoFiltered": "(filtrado de un total de _MAX_ registros)",
            "sInfoPostFix": "",
            "sSearch": "Buscar:",
            "sUrl": "",
            "sInfoThousands": ",",
            "sLoadingRecords": "Cargando...",
            "oPaginate": {
                "sFirst": "<span class='fa fa-angle-double-left'></span>",
                "sLast": "<span class='fa fa-angle-double-right'></span>",
                "sNext": "<span class='fa fa-angle-right'></span>",
                "sPrevious": "<span class='fa fa-angle-left'></span>"
            },
            "oAria": {
                "sSortAscending": ": Activar para ordenar la columna de manera ascendente",
                "sSortDescending": ": Activar para ordenar la columna de manera descendente"
            }
        },
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchdata'
            },
            dataSrc: ""
        },
        columns: [
            {"data": "id"},
            {"data": "name"},
            {"data": "stock"},
            {"data": "type_stock"},
            {"data": "quantity"},
            {"data": "id"}
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="#" rel="edit" class="btn btn-warning"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="#" rel="delete" class="btn btn-danger"><i class="fas fa-trash-alt"></i></a> ';
                    buttons += '<a href="#" rel="detail" class="btn btn-info"><i class="fas fa-folder-open"></i></a> ';

                    return buttons;
                }
            },
            {
                targets: [2],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    if (data >=20){
                        button = '<span class="badge badge-success">'+ data +'</span>';
                    }else if (data >=10){
                        button = '<span class="badge badge-warning">'+ data +'</span>';
                    }else{
                        button = '<span class="badge badge-danger">'+ data +'</span>';
                    }
                    return button;
                }
            },
            {
                targets: [5],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {

                    var date_1 = new Date();
                    var date_2 = new Date(data);
                    var day_as_milliseconds = 86400000;
                    var diff_in_millisenconds = date_2 - date_1;
                    var diff_in_days = diff_in_millisenconds / day_as_milliseconds;

                    if (diff_in_days >= 14) {
                        button = '<span class="badge badge-success">'+ data +'</span>';
                    }else if (diff_in_days >= 8){
                        button = '<span class="badge badge-warning">'+ data +'</span>';
                    }else if(diff_in_days <= 7){
                        button = '<span class="badge badge-danger">'+ data +'</span>';
                    }

                    return button;
                }
            },
        ],
        initComplete: function (settings, json) {
            
        }
    });
}

$(function () {

    modal_title = $('.modal-header');
    getData(); 

    /** EDIT PRODUCT */
    $('#data tbody').on('click', 'a[rel="edit"]', function () {
        $('#form1')[0].reset();        
        modal_title.find('h5').html('Editar Producto');
        var tr = tblCate.cell($(this).closest('td, li')).index();
        var data = tblCate.row(tr.row).data();
        $('input[name="action"]').val('edit');
        $('input[name="id"]').val(data.id);
        $('input[name="name"]').val(data.name);
        $('input[name="stock"]').val(data.stock);
        $('select[name="type_stock"]').val(data.type_stock);
        $('input[name="quantity"]').val(data.quantity);

        function type_unity() {
            option = $('select[name="type_stock"]').val();
            console.log(option);
            if ( option != 'cantidad' ) {
                option = document.querySelector('#div_hidden').removeAttribute('hidden','hidden');
            }else{
                option = document.querySelector('#div_hidden').setAttribute('hidden','hidden');
            };
        };
        $('#type_stock').change(function(){
            type_unity()
        });
        type_unity()

        $('#ModalNew').modal('show');
    });

    /** ADD PRODUCT */
    $('.btn-add').on('click', function () {
        $('input[name="action"]').val('add')
        modal_title.find('h5').html('Registrar Producto')
        $('#form1')[0].reset();
        stock = document.querySelector('#input_hidden').setAttribute('hidden','hidden');
        function type_unity() {
            option = $('select[name="type_stock"]').val();
            if ( option != 'cantidad' ) {
                option = document.querySelector('#div_hidden').removeAttribute('hidden','hidden');
            }else{
                option = document.querySelector('#div_hidden').setAttribute('hidden','hidden');
            };
        };
        $('#type_stock').change(function(){
            type_unity()
        });
        type_unity()

        $('#ModalNew').modal('show');

    });

    /** DELETE PRODUCT */
    $('#data tbody').on('click', 'a[rel="delete"]', function () {
        
        var tr = tblCate.cell($(this).closest('td, li')).index();
        var data = tblCate.row(tr.row).data();
        var parameters = new FormData();
        parameters.append('action', 'delete')
        parameters.append('id', data.id)
        submit_with_ajax(window.location.pathname,'Notifiación', '¿Estas seguro de eliminar este registro?', parameters, function () {
            
            tblCate.ajax.reload();
            toastr.success('Se ha eliminado correctamente');
            
        });
    });

    /** FORM SUBMIT */
    $('#form1').on('submit', function (e) {
        e.preventDefault();
        var parameters = new FormData(this);
        submit_with_ajax(window.location.pathname,'Notifiación', '¿Estas seguro de realizar esta accion?', parameters, function () {
            $('#ModalNew').modal('hide');
            tblCate.ajax.reload();
                estado_sms = document.querySelector("#status").getAttribute('value');
                if (estado_sms == "add") {
                    toastr.success('Se ha registrado correctamente');
                }else if (estado_sms == "edit"){
                    toastr.success('Se ha actualizado correctamente');
                }else{
                    toastr.success('Se ha eliminado correctamente');
                };                
        });    
    });
    
});


function open_modal(url) {
    
    $("#Modal_Detail").load(url, function() {

        $(this).modal({
            backdrop:'static',
            keyboard: false
        });

        $(this).modal('show');
    });
    return false;
};

function close_modal() {
    $('#Modal_Detail').modal('hide');
    return false;
};

    /** DETAIL */
    $('#data tbody').on('click', 'a[rel="detail"]', function () {
        var tr = tblCate.cell($(this).closest('td, li')).index();
        var data = tblCate.row(tr.row).data();
        url = 'detail/' + data.id + '/' 

        open_modal(url)

    });
