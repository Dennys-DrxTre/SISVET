
var tblCate;
var modal_title;
var messages;

/** TABLE PET */
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
            {"data": "date_nac"},
            {"data": "gender"},
            {"data": "weight"},
            {"data": "specie"},
            {"data": "client.dni"},
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
                    buttons += '<a href="#" rel="detail" class="btn btn-info"><i class="fas fa-folder-open"></i></a> ';
                    buttons += '<a href="#" rel="pdf" id="pdfs" class="btn bg-dark"><i class="fas fa-file-pdf"></i></a> ';
                    
                    if (data == '<span class="badge badge-success btn-colores">Activado</span>'){
                        buttons += '<a href="#" rel="btn-estado" class="btn btn-colores"><i class="fas fa-power-off"></i></a> ';
                    }else if (data == '<span class="badge badge-dark">Desactivado</span>'){
                        buttons += '<a href="#" rel="btn-estado" class="btn btn-dark"><i class="fas fa-power-off"></i></a> ';
                    }
                   
                    return buttons;
                }
            },
            {
                targets: [4],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {

                    data = `<span class="badge badge-dark">${data} Kg</span>`;
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


    /** ADD PET */
    $('.btn-add').on('click', function () {
        $('input[name="action"]').val('add')
        modal_title.find('h5').html('Registrar Mascota')
        $('form')[0].reset();
        $('select[name="client"]').val(null).trigger('change');
        $('#ModalNew').modal('show');

    });

    /** EDIT PET */
    $('#data tbody').on('click', 'a[rel="edit"]', function () {
        $('form')[0].reset();        
        modal_title.find('h5').html('Editar Mascota');
        var tr = tblCate.cell($(this).closest('td, li')).index();
        var data = tblCate.row(tr.row).data();
        $('input[name="action"]').val('edit');
        $('input[name="id"]').val(data.id);
        $('select[name="client"]').val(data.client.id);
        select_tittle = document.querySelector('.select2-selection__rendered').innerHTML = data.client.dni;
        $('input[name="name"]').val(data.name);
        $('select[name="gender"]').val(data.gender);
        $('input[name="race"]').val(data.race);
        $('input[name="weight"]').val(data.weight);
        $('input[name="specie"]').val(data.specie);
        $('input[name="date_up"]').val(data.date_up);
        $('input[name="date_nac"]').val(data.date_nac);
        $('input[name="substitute"]').val(data.substitute);
        if (data.status == '<span class="badge badge-success btn-colores">Activado</span>') {
            input = document.querySelector('.status').setAttribute('checked','checked');
            
        }else{
            input = document.querySelector('.status').removeAttribute('checked','checked');
        };
        $('#ModalNew').modal('show');
    });

    /** DELETE PET */
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

    /** PDF PET */
    $('#data tbody').on('click', 'a[rel="pdf"]', function () {
        var tr = tblCate.cell($(this).closest('td, li')).index();
        var data = tblCate.row(tr.row).data();
        window.open('/reports/consultation/' + data.id + '/');
    });

    /** STATUS PET */
    $('#data tbody').on('click', 'a[rel="btn-estado"]', function () {
        
        var tr = tblCate.cell($(this).closest('td, li')).index();
        var data = tblCate.row(tr.row).data();
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
