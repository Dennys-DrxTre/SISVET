
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
            {"data": "pet.name"},
            {"data": "motive"},
            {"data": "symptom"},
            {"data": "temperature"},
            {"data": "diag_pre"},
            {"data": "diag_def"},
            {"data": "fre_car"},
            {"data": "fre_res"},
            {"data": "examination"},
            {"data": "status"},
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

                    if (data == '<span class="badge badge-success btn-colores">Activado</span>'){
                        buttons += '<a href="#" rel="btn-estado" class="btn btn-colores"><i class="fas fa-power-off"></i></a> ';
                    }else if (data == '<span class="badge badge-dark">Desactivado</span>'){
                        buttons += '<a href="#" rel="btn-estado" class="btn btn-dark"><i class="fas fa-power-off"></i></a> ';
                    }
                   
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
    /** DETAIL Consulta */
    $('#data tbody').on('click', 'a[rel="detail"]', function () {
        
        modal_title.find('h4').html('Detalle de la Consulta');
        var tr = tblCate.cell($(this).closest('td, li')).index();
        var data = tblCate.row(tr.row).data();
        id = document.querySelector('#detail-id').textContent = data.id;
        motivo = document.querySelector('#detail-client').textContent = data.motive;
        sintoma = document.querySelector('#detail-substitute').textContent = data.symptom;
        name_pet = document.querySelector('#detail-name1').textContent = data.pet.name;
        gender = document.querySelector('#detail-gender').textContent = data.pet.gender;
        race = document.querySelector('#detail-race').textContent = data.pet.race;
        specie = document.querySelector('#detail-specie').textContent = data.pet.specie;
        date_nace = document.querySelector('#detail-date_nac').textContent = data.temperature;
        fr_car = document.querySelector('#detail-fre_car').textContent = data.fre_car;
        fr_res = document.querySelector('#detail-fre_res').textContent = data.fre_res;
        diag_pre = document.querySelector('#detail-date_up').textContent = data.diag_pre;
        Email = document.querySelector('#detail-diag_def').textContent = data.diag_def;
        examen = document.querySelector('#detail-examen').textContent = data.examination;
        new_cita = document.querySelector('#detail-cita').textContent = data.date_u;
        $('#Modal_Detail').modal('show');

        /** DETAIL PET EDIT */
        $('#Modal_Detail').on('click', 'a[rel="edit"]', function () {
        
            modal_title.find('h5').html('Editar Mascota');
            $('form')[0].reset();        
            $('input[name="action"]').val('edit');
            $('input[name="id"]').val(data.id);
            $('textarea[name="motive"]').val(data.motive);
            $('textarea[name="symptom"]').val(data.symptom);
            $('select[name="pet"]').val(data.pet.id);
            select_tittle = document.querySelector('.select2-selection__rendered').innerHTML = data.pet.name;
            $('textarea[name="temperature"]').val(data.temperature);
            $('textarea[name="diag_pre"]').val(data.diag_pre);
            $('textarea[name="diag_def"]').val(data.diag_def);
            $('textarea[name="fre_car"]').val(data.fre_car);
            $('textarea[name="fre_res"]').val(data.fre_res);
            $('input[name="date_c"]').val(data.date_c);
            $('input[name="date_u"]').val(data.date_u);
            $('textarea[name="examination"]').val(data.examination);
            $('input[name="total"]').val(data.total);
            
            if (data.status == '<span class="badge badge-success btn-colores">Activado</span>') {
                input = document.querySelector('.status').setAttribute('checked','checked');
                
            }else{
                input = document.querySelector('.status').removeAttribute('checked','checked');
            };
            $('#Modal_Detail').modal('hide');
            $('#ModalNew').modal('show');
        });

    });  

    /** DETAIL PET DELETE */
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

    /** ADD PET */
    $('.btn-add').on('click', function () {
        $('input[name="action"]').val('add')
        modal_title.find('h5').html('Registrar Consulta')
        $('form')[0].reset();
        $('#ModalNew').modal('show');

    });

    /** EDIT PET */
    $('#data tbody').on('click', 'a[rel="edit"]', function () {
        $('form')[0].reset();        
        modal_title.find('h5').html('Editar Consulta');
        var tr = tblCate.cell($(this).closest('td, li')).index();
        var data = tblCate.row(tr.row).data();
        $('input[name="action"]').val('edit');
        $('input[name="id"]').val(data.id);
        $('textarea[name="symptom"]').val(data.symptom);
        $('textarea[name="motive"]').val(data.motive);
        $('select[name="pet"]').val(data.pet.id);
        select_tittle = document.querySelector('.select2-selection__rendered').innerHTML = data.pet.name;
        $('textarea[name="temperature"]').val(data.temperature);
        $('textarea[name="diag_pre"]').val(data.diag_pre);
        $('textarea[name="diag_def"]').val(data.diag_def);
        $('textarea[name="fre_car"]').val(data.fre_car);
        $('textarea[name="fre_res"]').val(data.fre_res);
        $('input[name="date_c"]').val(data.date_c);
        $('input[name="date_u"]').val(data.date_u);
        $('textarea[name="examination"]').val(data.examination);
        $('input[name="total"]').val(data.total);
        // $('input[name="substitute"]').val(data.substitute);
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

