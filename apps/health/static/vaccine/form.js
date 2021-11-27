var modal_title;
var tblCate;
var vents = {
    items : {
        product: '',
        date: '',
        description: '',
        quantity: 0,
        quantity_usage: 0,
        quantity_for_pet: 0,
        pets: []
    },
    get_ids: function () {
        var ids =  [];
        $.each(this.items.pets, function (key, value) {
            ids.push(value.id);
        });
        return ids;
    },
    calculate_invoice: function () {
        var quantity_for_pet = $('input[name="quantity_pet"]').val();
        var quantity = $('input[name="quantity"]').val();
        $.each(this.items.pets, function (pos, dict) {
            dict.quantity = parseInt(quantity_for_pet); 
        });
        this.items.quantity = parseInt(quantity) - parseInt(quantity_for_pet);
        this.items.quantity_usage += parseInt(quantity_for_pet); 
        this.items.quantity_for_pet = parseInt(quantity_for_pet);
        $('input[name="quantity"]').val(this.items.quantity);


    },
    add: function (item) {
        this.items.pets.push(item);
        this.calculate_invoice();
        this.list()

    },
    list: function () {
        
        tblCate = $('#data2').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            ordering:  false,
            searching: false,
            paging: false, 
            "language": {
                "sProcessing": "Procesando...",
                "sLengthMenu": "Mostrar _MENU_ registros",
                "sZeroRecords": "No se encontraron resultados",
                "sEmptyTable": "Ningún dato disponible en esta tabla",
                "sInfo": "Mostrando _START_ al _END_ de un total de _TOTAL_ registros",
                "sInfoEmpty": "Mostrando 0 al 0 de un total de 0 registros",
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
            data: this.items.pets,
            columns: [
                {"data": "name"},
                {"data": "client"},
                {"data": "specie"},
                {"data": "quantity"},
                {"data": "id"},
            ],
            columnDefs: [
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {

                        buttons = '<a href="#" rel="delete" class="btn btn-danger"><i class="fas fa-trash-alt"></i></a> ';                       
                        return buttons;
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row, meta) {                        

                        return '<input type="number" readonly value="'+ parseInt(data) +'" name="quantity_det" class="form-control form-control-sm event_input1" autocomplete="off">';
                    }
                },
            ],
            initComplete: function (settings, json) {

            },
        });

    },
};

function formatRepo(repo) {
    if (repo.loading) {
        return repo.text;
    }

    var option = $(
        '<div class="col text-left shadow-sm">' +
        '<p style="margin-bottom: 0;">' +
        '<b>Nombre:</b> ' + repo.name+ '<br>' +
        '<b>Dueño:</b> ' + repo.client + '<br>' +
        '<b>Especie:</b> <span class="badge badge-dark">'+repo.specie+'</span>'+
        '</p>' +
        '</div>');

    return option;
}

$(function () {
    // auto complete search
    $('select[name="search"]').select2({
        theme: "bootstrap4",
        language: "es",
        allowClear: true,
        ajax: {
            delay: 250,
            type: "POST", 
            url: window.location.pathname,
            data: function (params) {
                var queryParameters = {
                    term: params.term,
                    action: "search_pets",
                    ids: JSON.stringify(vents.get_ids())
                }
                return queryParameters;
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Ingrese una mascota', 
        minimumInputLength: 1,
        templateResult: formatRepo,
    }).on('select2:select', function (e) {
        if (vents.items.pets.length > 0) {
            if (vents.items.quantity <= 0){
                toastr.error('la cantidad disponible del producto no puede ser superado');
                return false;
            } 
        }

        var data = e.params.data;

        vents.add(data);
        $(this).val('').trigger('change.select2');

    });

    // event inputs
    $('#data2 tbody').on('click', 'a[rel="delete"]', function () {
        var tr = tblCate.cell($(this).closest('td, li')).index();
        submit_action('Notificacion', '¿Desea eliminar esta mascota de tu detalle?', function () {
            quantity_for_pet = $('input[name="quantity_pet"]').val()
            vents.items.quantity += parseInt(quantity_for_pet);
            vents.items.quantity_usage -= parseInt(quantity_for_pet);
            $('input[name="quantity"]').val(parseInt(vents.items.quantity));
            vents.items.pets.splice(tr.row, 1);
            vents.list();
            toastr.success('Eliminado Correactamente')
        })

    });

    $('a[rel="btn_delete"]').on('click', function () {
        if (vents.items.pets.length === 0) return false;
        submit_action('Notificacion', '¿Desea eliminar todos las mascotas de tu detalle?', function () {
            quantity_for_pet = $('input[name="quantity_pet"]').val()
            const sum = parseInt(vents.items.pets.length) * parseInt(quantity_for_pet)
            vents.items.quantity += parseInt(sum);
            vents.items.quantity_usage -= parseInt(sum);
            $('input[name="quantity"]').val(parseInt(vents.items.quantity));
            vents.items.pets = [];
            vents.list();
            toastr.success('Eliminado Correactamente')
        })
    });

    // event submit
    $('form').on('submit', function (e) {
        e.preventDefault();
        
        if (vents.items.pets.length === 0) {
            toastr.error('Debe al menos tener una mascota en su detalle de jornada de vacunación');
            return false;
        }

        vents.items.product = $('select[name="product"]').val();
        vents.items.date = $('input[name="date"]').val();
        vents.items.description = $('textarea[name="description"]').val();
        vents.items.quantity = $('input[name="quantity"]').val();
        if (vents.items.quantity < 0) {s
            vents.items.quantity = 0;
        }
        vents.items.quantity_for_pet = $('input[name="quantity_pet"]').val();



        var parameters = new FormData();
        parameters.append('action', $('input[name="action"]').val());
        parameters.append('vents', JSON.stringify(vents.items));

        submit_with_ajax(window.location.pathname,'Notifiación', '¿Estas seguro de realizar esta accion?', parameters, function () {
            window.location.replace('/health/listado_jornada_vacunacion/');
        });    
    });

    $('.select22').select2({
        theme: 'bootstrap4',
        placeholder:'Seleccione el producto',
        language: 'es',
        allowClear: true
    });


    $("input[name='quantity']").TouchSpin({
        verticalbuttons: true,
        verticalupclass: 'glyphicon glyphicon-plus',
        verticaldownclass: 'glyphicon glyphicon-minus',
        step: 1,
        initval: 1,
        min: 0,
    });

    $("input[name='quantity_pet']").TouchSpin({
        verticalbuttons: true,
        verticalupclass: 'glyphicon glyphicon-plus',
        verticaldownclass: 'glyphicon glyphicon-minus',
        step: 1,
        min: 0,
        initval: 1
    });

    $('input[name="date"]').daterangepicker({
        singleDatePicker: true,
        showDropdowns: true,
        minYear: 2020,
        maxYear: parseInt(moment().format('YYYY'),10),
        locale: {format: 'YYYY-MM-DD'}
    });
})

function PagePrevious() {
    window.history.back();
}