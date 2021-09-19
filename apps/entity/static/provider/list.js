
var tblCate;
var modal_title;
var messages;

/** TABLE PROVIDER */
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
            "sInfoEmpty": "Mostrando del 0 al 0 de un total de 0 registros",
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
            {"data": "rif"},
            {"data": "mobile"},
            {"data": "tlf"},
            {"data": "Email"},
            {"data": "status"},
            {"data": "status"}
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="#" rel="edit" class="btn btn-warning"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="#" rel="delete" class="btn btn-danger"><i class="fas fa-trash-alt"></i></a> ';
                    if (data == '<span class="badge badge-success btn-colores">Activado</span>'){
                        buttons += '<a href="#" rel="btn-estado" class="btn btn-colores"><i class="fas fa-power-off"></i></a> ';
                    }else if (data == '<span class="badge badge-dark">Desactivado</span>'){
                        buttons += '<a href="#" rel="btn-estado" class="btn btn-dark"><i class="fas fa-power-off"></i></a> ';
                    }
                   
                    return buttons;
                }
            },
            {
                targets: [0],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {

                   button = '<strong><a rel="detail" class="product-title text-success btn-detail" href="#">'+data+'</a></strong>'
                    return button;
                }
            },
            {
                targets: [2,3,4,5],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {

                    if (data){
                        data = data;
                    }else{
                        data = '<span class="badge badge-dark"> Vacio </span>';
                    }
                    return data;

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
    /** DETAIL PROVIDER */
    $('#data tbody').on('click', 'a[rel="detail"]', function () {
        
        modal_title.find('h4').html('Detalle del Proveedor');
        var tr = tblCate.cell($(this).closest('td, li')).index();
        var data = tblCate.row(tr.row).data();
        id = document.querySelector('#detail-id').textContent = data.id;
        rif = document.querySelector('#detail-rif').textContent = data.rif;        
        name_pro = document.querySelector('#detail-name').textContent = data.name;
        mobile = document.querySelector('#detail-mobile').textContent = data.mobile;
        tlf = document.querySelector('#detail-tlf').textContent = data.tlf;
        name_com = document.querySelector('#detail-name_com').textContent = data.name;
        Email = document.querySelector('#detail-Email').textContent = data.Email;
        if (data.status == '<span class="badge badge-success btn-colores">Activado</span>') {
            input = document.querySelector('#status-btn').setAttribute('class','btn btn-colores');
            
        }else{
            input = document.querySelector('#status-btn').setAttribute('class','btn btn-dark');
        };
        $('#Modal_Detail').modal('show');

        /** DETAIL PROVIDER EDIT */
        $('#Modal_Detail').on('click', 'a[rel="edit"]', function () {
        
            modal_title.find('h5').html('Editar Cliente');
            $('form')[0].reset();
            $('input[name="action"]').val('edit');
            $('input[name="id"]').val(data.id);
            $('input[name="rif"]').val(data.rif);
            $('input[name="name"]').val(data.name);
            $('input[name="Email"]').val(data.Email);
            $('input[name="mobile"]').val(data.mobile);
            $('input[name="tlf"]').val(data.tlf);
            if (data.status == '<span class="badge badge-success btn-colores">Activado</span>') {
                input = document.querySelector('.status').setAttribute('checked','checked');
                
            }else{
                input = document.querySelector('.status').removeAttribute('checked','checked');
            };
            
            $('#Modal_Detail').modal('hide');
            $('#ModalNew').modal('show');
        });

    });  

    /** DETAIL PROVIDER DELETE */
    $('#Modal_Detail').on('click', 'a[rel="delete"]', function () {
        id = document.querySelector('#detail-id').textContent;
        var parameters = new FormData();
        parameters.append('action', 'delete')
        
        parameters.append('id', id)
        console.log(parameters)
        submit_with_ajax(window.location.pathname,'Notifiación', '¿Estas seguro de eliminar este registro?', parameters, function () {
            
            tblCate.ajax.reload();
            toastr.success('Se ha eliminado correctamente');
            
        });
        $('#Modal_Detail').modal('hide');
    });  
    
    /** DETAIL PROVIDER STATUS */
    $('#Modal_Detail').on('click', 'a[rel="btn-estado"]', function () {
        
        id = document.querySelector('#detail-id').textContent;
        $('#Modal_Detail').modal('hide');
        var parameters = new FormData();
        parameters.append('action', 'btn-estado')
        parameters.append('id', id)
        submit_with_ajax(window.location.pathname,'Notifiación', '¿Estas seguro de cambiar el estado de este registro?', parameters, function () {
            
            tblCate.ajax.reload();
            toastr.success('El estado se ha actualizado correctamente');

        });
    });

    /** ADD PROVIDER */
    $('.btn-add').on('click', function () {
        $('form')[0].reset();
        $('input[name="action"]').val('add')
        modal_title.find('h5').html('Registrar Cliente')
        input = document.querySelector('.status').setAttribute('checked','checked');
        $('#ModalNew').modal('show');

    });

    /** EDIT PROVIDER */
    $('#data tbody').on('click', 'a[rel="edit"]', function () {
        $('form')[0].reset();        
        modal_title.find('h5').html('Editar Cliente');
        var tr = tblCate.cell($(this).closest('td, li')).index();
        var data = tblCate.row(tr.row).data();
        $('input[name="action"]').val('edit');
        $('input[name="id"]').val(data.id);
        $('input[name="rif"]').val(data.rif);
        $('input[name="name"]').val(data.name);
        $('input[name="Email"]').val(data.Email);
        $('input[name="mobile"]').val(data.mobile);
        $('input[name="tlf"]').val(data.tlf);
        if (data.status == '<span class="badge badge-success btn-colores">Activado</span>') {
            input = document.querySelector('.status').setAttribute('checked','checked');
            
        }else{
            input = document.querySelector('.status').removeAttribute('checked','checked');
        };
        $('#ModalNew').modal('show');
    });

    /** DELETE PROVIDER */
    $('#data tbody').on('click', 'a[rel="delete"]', function () {
        
        var tr = tblCate.cell($(this).closest('td, li')).index();
        var data = tblCate.row(tr.row).data();
        console.log(data)
        var parameters = new FormData();
        parameters.append('action', 'delete')
        parameters.append('id', data.id)
        submit_with_ajax(window.location.pathname,'Notifiación', '¿Estas seguro de eliminar este registro?', parameters, function () {
            
            tblCate.ajax.reload();
            toastr.success('Se ha eliminado correctamente');
            
        });
    });

    /** STATUS PROVIDER */
    $('#data tbody').on('click', 'a[rel="btn-estado"]', function () {
        
        var tr = tblCate.cell($(this).closest('td, li')).index();
        var data = tblCate.row(tr.row).data();
        console.log(data)
        var parameters = new FormData();
        parameters.append('action', 'btn-estado')
        parameters.append('id', data.id)
        submit_with_ajax(window.location.pathname,'Notifiación', '¿Estas seguro de cambiar el estado de este registro?', parameters, function () {
            
            tblCate.ajax.reload();
            toastr.success('El estado se ha actualizado correctamente');
            
        });
    });


    /** FORM SUBMIT */
    $('form').on('submit', function (e) {
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

$(function () {
    $('.select2').select2({
        theme: 'bootstrap4',
        language: 'es',
        placeholder: 'Selecionar Cliente',
        allowClear: true
        
    });
});
