var modal_title;
var tblCate;
var vents = {
    items : {
        provider: '',
        total: 0.00,
        total_bs: 0.00,
        iva: 0.00,
        price_dollar: 0.00,
        subtotal: 0.00,
        type_bs: 'Compra',
        products: []
    },
    calculate_invoice: function () {
        var subtotal = 0.00;
        var iva = $('input[name="iva"]').val();
        var price_dollar = $('input[name="price_dollar"]').val();
<<<<<<< HEAD
        
=======

>>>>>>> b0891a40af8565bd3fc0e1b635d55a867dbce1e5
        $.each(this.items.products, function (pos, dict) {
            dict.total = parseInt(dict.stock) * parseFloat(dict.price_buy);
            dict.profit = dict.price_sale - dict.price_buy;
            if ( parseFloat(dict.profit) < parseFloat(0.00)) {
                dict.profit = 0.00;
            }else{
                dict.profit = dict.profit;
            };
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
<<<<<<< HEAD
=======


>>>>>>> b0891a40af8565bd3fc0e1b635d55a867dbce1e5
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

                        return '<input type:"text" value=" '+ data.toFixed(2) +' " name="total_p" readonly class="form-control form-control-sm" autocomplete="off">';
                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {

                        return '<input type:"text" value=" '+ data.toFixed(2) +' " name="profit_p"  readonly class="form-control form-control-sm" autocomplete="off">';
                    }
                },
                {
                    targets: [-4],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {


                        return '<input type="text" value="'+ data +'" name="stock" class="form-control form-control-sm event_input1" autocomplete="off">';
                    }
                },
                {
                    targets: [-6],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {

                        return '<input type="text" value="'+data.toFixed(2)+'"  name="price_buy" class="form-control form-control-sm event_input2" autocomplete="off">';
                    }
                },
                {
                    targets: [-5],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {

                        return '<input type="text" value="'+data.toFixed(2)+'" name="price_sale" class="form-control form-control-sm event_input3" autocomplete="off">';
                    }
                },
                {
                    targets: [-8],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row, index) {
                        return '<input type="text" readonly value="'+data+'" name="date_conquered" class="form-control form-control-sm date_picker"  autocomplete="off">';
                    
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
                    max: 1000
                });
                $(row).find("input[name='price_buy']").TouchSpin({
                    verticalbuttons: true,
                    verticalupclass: 'glyphicon glyphicon-plus',
                    verticaldownclass: 'glyphicon glyphicon-minus',
                    step: 0.01,
                    decimals: 2,
                    boostat: 5,
                    maxboostedstep: 10,
                    min: 0,
                    max: 1000000
                });
                $(row).find("input[name='price_sale']").TouchSpin({
                    verticalbuttons: true,
                    verticalupclass: 'glyphicon glyphicon-plus',
                    verticaldownclass: 'glyphicon glyphicon-minus',
                    step: 0.01,
                    decimals: 2,
                    boostat: 5,
                    maxboostedstep: 10,
                    min: 0,
                    max: 1000000
                });
                $(row).find("input[name='date_conquered']").datepicker({
                    dateFormat: 'yy-mm-dd',
                    'language': 'es'
                });
            },
            initComplete: function (settings, json) {

            },
        });

    },
};
$(function () {

    // auto complete search
    $('input[name="search"]').autocomplete({
        source: function (request, response) {
            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'search_products',
                    'term': request.term
                },
                dataType: 'json',
            }).done(function (data) {
                response(data);
            }).fail(function (jqXHR, textStatus, errorThrown) {
                
            }).always(function (data) {
                
            });
        },
        delay: 500,
        minLength: 1,
        select: function (event, ui) {
            event.preventDefault();

            ui.item.stock =1
            ui.item.price_sale =0.00
            ui.item.price_buy =0.00
            ui.item.date_conquered = moment().format('YYYY-MM-DD')
            ui.item.profit =0.00

            ui.item.total =0

            console.log(vents.items);
            vents.add(ui.item);
            $(this).val('');
        } 
    })

    // event inputs
    $('#data2 tbody').on('click', 'a[rel="delete"]', function () {
        var tr = tblCate.cell($(this).closest('td, li')).index();
        submit_action('Notificacion', '¿Desea eliminar el producto de tu detalle?', function () {
            vents.items.products.splice(tr.row, 1);
            vents.list();
            toastr.success('Eliminado Correactamente')
        })

    });

    $('.btn_delete').on('click', function () {
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
        $('td:eq(6)', tblCate.row(tr.row).node()).html('<input type:"text" value=" '+ vents.items.products[tr.row].total.toFixed(2) +' " name="total_p" readonly class="form-control form-control-sm" autocomplete="off">')

    });
    $('#data2 tbody').on('change keyup', '.event_input2', function () {
        var pb = $(this).val();
        var tr = tblCate.cell($(this).closest('td, li')).index();
        var data = tblCate.row(tr.row).data();
        vents.items.products[tr.row].price_buy = parseFloat(pb);
        vents.items.products[tr.row].profit = parseFloat(data.profit);
        if ( parseFloat(vents.items.products[tr.row].price_buy) > parseFloat(vents.items.products[tr.row].price_sale) ){
            toastr.error("ADVERTENCIA: El Precio de Venta no puede ser menor al Precio de Compra.");
        };
        vents.calculate_invoice();        
        $('td:eq(5)', tblCate.row(tr.row).node()).html('<input type:"text" value=" '+ vents.items.products[tr.row].profit.toFixed(2) +' " name="profit_p"  readonly class="form-control form-control-sm" autocomplete="off">')
        $('td:eq(6)', tblCate.row(tr.row).node()).html('<input type:"text" value=" '+ vents.items.products[tr.row].total.toFixed(2) +' " name="total_p" readonly class="form-control form-control-sm" autocomplete="off">')

    });
    $('#data2 tbody').on('change keyup', '.event_input3', function () {
        var ps = $(this).val();
        var tr = tblCate.cell($(this).closest('td, li')).index();
        var data = tblCate.row(tr.row).data();
        vents.items.products[tr.row].price_sale = parseFloat(ps);
        vents.items.products[tr.row].profit = parseFloat(data.profit);
        if ( parseFloat(vents.items.products[tr.row].price_buy) > parseFloat(vents.items.products[tr.row].price_sale) ){
            toastr.error("ADVERTENCIA: El Precio de Venta no puede ser menor al Precio de Compra.");
        };
        vents.calculate_invoice();
        $('td:eq(5)', tblCate.row(tr.row).node()).html('<input type:"text" value=" '+ vents.items.products[tr.row].profit.toFixed(2) +' " name="profit_p"  readonly class="form-control form-control-sm" autocomplete="off">')

    });
    $('#data2 tbody').on('change', '.date_picker', function () {
        var date_conquered = $(this).val();
        var tr = tblCate.cell($(this).closest('td, li')).index();
        vents.items.products[tr.row].date_conquered = date_conquered;
        vents.calculate_invoice();
        $('td:eq(0)', tblCate.row(tr.row).node()).html('<input type="text" value="'+ vents.items.products[tr.row].date_conquered +'" readonly name="date_conquered" class="form-control form-control-sm date_picker"  autocomplete="off">')

    });

    // event submit
    $('form').on('submit', function (e) {
        e.preventDefault();
        
        if (vents.items.products.length === 0) {
            toastr.error('Debe al menos tener un producto en su detalle de compra');
            return false;
        }

        vents.items.provider = $('select[name="provider"]').val();

        var parameters = new FormData();
        parameters.append('action', $('input[name="action"]').val());
        parameters.append('vents', JSON.stringify(vents.items));

        submit_with_ajax(window.location.pathname,'Notifiación', '¿Estas seguro de realizar esta accion?', parameters, function () {
            window.location.replace('/inventory/listado_compras/');
        });    
    });

    $('.select22').select2({
        theme: 'bootstrap4',
        placeholder:'Seleccione el proveedor',
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
    }).on('keyup', function () {
        vents.calculate_invoice();
    }).val(0.16);

<<<<<<< HEAD
=======
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
>>>>>>> b0891a40af8565bd3fc0e1b635d55a867dbce1e5

});

function PagePrevious() {
    window.history.back();
}