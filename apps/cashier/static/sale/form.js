var modal_title;
var tblCate;
var vents = {
    items : {
        client: '',
        total: 0.00,
        total_bs: 0.00,
        price_dollar: 0.00,
        iva: 0.00,
        subtotal: 0.00,
        type_bs: 'Venta',
        products: []
    },
    get_ids: function () {
        var ids =  [];
        $.each(this.items.products, function (key, value) {
            ids.push(value.id);
        });
        return ids;
    },
    calculate_invoice: function () {
        var subtotal = 0.00;
        var iva = $('input[name="iva"]').val();
        var price_dollar = $('input[name="price_dollar"]').val();
        $.each(this.items.products, function (pos, dict) {
            dict.total = dict.stock * dict.price_sale;
            dict.profit = dict.profit;

            subtotal += dict.total;

        });
        this.items.subtotal = subtotal;
        this.items.iva = iva;
        iva = this.items.subtotal * iva;
        this.items.total = this.items.subtotal + iva;
        this.items.total_bs = this.items.subtotal + iva;
        this.items.total_bs = this.items.total_bs * price_dollar;
        this.items.price_dollar = parseFloat(price_dollar).toFixed(2);

        $('input[name="sub_total"]').val(this.items.subtotal.toFixed(2))
        $('input[name="total"]').val(this.items.total.toFixed(2))
        $('input[name="total_bs"]').val(this.items.total_bs.toFixed(2))

    },
    add: function (item) {
        this.items.products.push(item);
        this.list()

    },
    list: function () {
        this.calculate_invoice();
        
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
            data: this.items.products,
            columns: [
                {"data": "date_conquered"},
                {"data": "name"},
                {"data": "price_buy"},
                {"data": "price_sale"},
                {"data": "stock"},
                {"data": "profit"},
                {"data": "total"},
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
                    render: function (data, type, row) {

                        return '$'+parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {

                        return '$'+parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-4],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row, meta) {                        

                        return '<input type="number" value="'+ parseInt(data) +'" name="stock" max="'+ parseInt(vents.items.products[meta.row].exist_stock) +'" class="form-control form-control-sm event_input1" autocomplete="off">';
                    }
                },
                {
                    targets: [-5],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {

                        return '$'+parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-6],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {

                        return '$'+parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-8],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row, index) {

                        return data;
                    }
                },

            ],
            rowCallback( row, data, displayNum, displayIndex, dataIndex ){
                $(row).find("input[name='stock']").TouchSpin({
                    verticalbuttons: true,
                    verticalupclass: 'glyphicon glyphicon-plus',
                    verticaldownclass: 'glyphicon glyphicon-minus',
                    step: 1,
                    min: 0,
                    max: parseInt(data.exist_stock),
                    initval: 1
                });
            },
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
        '<b>Fecha de Vencimiento:</b> ' + repo.date_conquered_2 + '<br>' +
        '<b>Disponibilidad del producto:</b> <span class="badge badge-dark">'+repo.stock+'</span>'+
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
                    action: "search_products",
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
        placeholder: 'Ingrese un producto', 
        minimumInputLength: 1,
        templateResult: formatRepo,
    }).on('select2:select', function (e) {
        var data = e.params.data;

        console.log(data);
        data.total =0;
        data.stock =1;

        vents.add(data);
        $(this).val('').trigger('change.select2');

    });

    // event inputs
    $('#data2 tbody').on('click', 'a[rel="delete"]', function () {
        var tr = tblCate.cell($(this).closest('td, li')).index();
        submit_action('Notificacion', '¿Desea eliminar el producto de tu detalle?', function () {
            vents.items.products.splice(tr.row, 1);
            vents.list();
            toastr.success('Eliminado Correactamente')
        })

    });

    $('a[rel="btn_delete"]').on('click', function () {
        if (vents.items.products.length === 0) return false;
        submit_action('Notificacion', '¿Desea eliminar todos los productos de tu detalle?', function () {
            vents.items.products = [];
            vents.list();
            toastr.success('Eliminado Correactamente')
        })
    });

    $('#data2 tbody').on('change keyup', '.event_input1', function () {
        var stock = $(this).val();
        var tr = tblCate.cell($(this).closest('td, li')).index();
         vents.items.products[tr.row].stock = parseInt(stock);
         vents.calculate_invoice();
         $('td:eq(6)', tblCate.row(tr.row).node()).html('$'+parseFloat(vents.items.products[tr.row].total).toFixed(2))
    });

    // event submit
    $('form').on('submit', function (e) {
        e.preventDefault();
        
        if (vents.items.products.length === 0) {
            toastr.error('Debe al menos tener un producto en su detalle de venta');
            return false;
        }

        vents.items.client = $('select[name="client"]').val();

        var parameters = new FormData();
        parameters.append('action', $('input[name="action"]').val());
        parameters.append('vents', JSON.stringify(vents.items));

        submit_with_ajax(window.location.pathname,'Notifiación', '¿Estas seguro de realizar esta accion?', parameters, function () {
            window.location.replace('/inventory/listado_ventas/');
        });    
    });

    $('.select22').select2({
        theme: 'bootstrap4',
        placeholder:'Seleccione el cliente',
        language: 'es'
    });


    $("input[name='iva']").TouchSpin({
        min: 0,
        max: 100,
        step: 0.01,
        decimals: 2,
        boostat: 5,
        maxboostedstep: 10,
        postfix: '%',
    }).on('change', function () {
        vents.calculate_invoice();
    }).val(0.16);

    $("input[name='price_dollar']").TouchSpin({
        verticalbuttons: true,
        verticalupclass: 'glyphicon glyphicon-plus',
        verticaldownclass: 'glyphicon glyphicon-minus',
        step: 0.01,
        decimals: 2,
        boostat: 5,
        maxboostedstep: 10,
        min: 0,
        initval: 0.00,
    });

})

function PagePrevious() {
    window.history.back();
}