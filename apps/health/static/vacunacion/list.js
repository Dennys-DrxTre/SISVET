
var tblCate;
var modal_title;
var messages;

/** TABLE VACUNACION */
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
            {"data": "pet.name"},
            {"data": "pet.client"},
            {"data": "name"},
            {"data": "description"},
            {"data": "date"},
            {"data": "total"},
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
                    return buttons;
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
    /** DETAIL VACUNACION */
    $('#data tbody').on('click', 'a[rel="detail"]', function () {
        
        modal_title.find('h4').html('Detalle de la Vacunacion');
        var tr = tblCate.cell($(this).closest('td, li')).index();
        var data = tblCate.row(tr.row).data();
        id = document.querySelector('#detail-id').textContent = data.id;
        desparacitante = document.querySelector('#detail-client').textContent = data.name;
        description = document.querySelector('#detail-substitute').textContent = data.description;
        total = document.querySelector('#detail-name1').textContent = data.pet.name;
        fecha = document.querySelector('#detail-gender').textContent = data.pet.gender; 
        race = document.querySelector('#detail-race').textContent = data.pet.race;
        specie = document.querySelector('#detail-specie').textContent = data.pet.specie;
        diag_pre = document.querySelector('#detail-date_up').textContent = data.date;
        Email = document.querySelector('#detail-diag_def').textContent = data.total;
        new_date = document.querySelector('#detail-new_date').textContent = data.new_date;
        $('#Modal_Detail').modal('show');

        /** DETAIL VACUNACION EDIT */
        $('#Modal_Detail').on('click', 'a[rel="edit"]', function () {
        
            modal_title.find('h5').html('Editar Vacunacion');
            $('form')[0].reset();        
            $('input[name="action"]').val('edit');
            $('input[name="id"]').val(data.id);
            $('textarea[name="name"]').val(data.name);
            $('textarea[name="description"]').val(data.description);
            $('select[name="pet"]').val(data.pet.id);
            select_tittle = document.querySelector('.select2-selection__rendered').innerHTML = data.pet.name;
            $('input[name="total"]').val(data.total);
            $('input[name="date"]').val(data.date);
            if (data.status == '<span class="badge badge-success btn-colores">Activado</span>') {
                input = document.querySelector('.status').setAttribute('checked','checked');
                
            }else{
                input = document.querySelector('.status').removeAttribute('checked','checked');
            };
            $('#Modal_Detail').modal('hide');
            $('#ModalNew').modal('show');
        });

    });  

    /** DETAIL VACUNACION DELETE */
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

    /** ADD VACUNACION */
    $('.btn-add').on('click', function () {
        $('input[name="action"]').val('add')
        modal_title.find('h5').html('Registrar Vacunacion')
        $('select[name="pet"]').val(null).trigger('change');
        $('form')[0].reset();
        $('#ModalNew').modal('show');

    });

    /** EDIT VACUNACION */
    $('#data tbody').on('click', 'a[rel="edit"]', function () {
        $('form')[0].reset();        
        modal_title.find('h5').html('Editar Vacunacion');
        var tr = tblCate.cell($(this).closest('td, li')).index();
        var data = tblCate.row(tr.row).data();
        $('input[name="action"]').val('edit');
        $('input[name="id"]').val(data.id);
        $('textarea[name="name"]').val(data.name);
        $('textarea[name="description"]').val(data.description);
        $('select[name="pet"]').val(data.pet.id).trigger('change');
        select_tittle = document.querySelector('.select2-selection__rendered').innerHTML = data.pet.name;
        $('input[name="total"]').val(data.total);
        $('input[name="date"]').val(data.date);
        // $('input[name="substitute"]').val(data.substitute);
        if (data.status == '<span class="badge badge-success btn-colores">Activado</span>') {
            input = document.querySelector('.status').setAttribute('checked','checked');
            
        }else{
            input = document.querySelector('.status').removeAttribute('checked','checked');
        };
        $('#ModalNew').modal('show');
    });

    /** DELETE VACUNACION */
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
        placeholder: 'Selecionar Mascota',
        allowClear: true
        
    });
});

