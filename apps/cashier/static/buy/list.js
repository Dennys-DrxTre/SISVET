
var tblCate;
var modal_title;
var messages;

/** TABLE CLIENT */
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
            {"data": "provider.name"},
            {"data": "type_bs"},
            {"data": "date"},
            {"data": "total"},
            {"data": "status"},
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="#" rel="edit" class="btn btn-warning"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="#" rel="delete" class="btn btn-danger"><i class="fas fa-trash-alt"></i></a> ';
                   
                    return buttons;
                }
            },
            {
                targets: [1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {

                   button = '<strong><a rel="detail" class="product-title text-success btn-detail" href="#">'+ data +'</a></strong>'
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
    /** DETAIL PRODUCT */
    $('#data tbody').on('click', 'a[rel="detail"]', function () {
        
        modal_title.find('h4').html('Detalle del Producto');
        var tr = tblCate.cell($(this).closest('td, li')).index();
        var data = tblCate.row(tr.row).data();
        id = document.querySelector('#detail-id').textContent = data.id;
        name_pro = document.querySelector('#detail-name1').textContent = data.name;
        name_pro2 = document.querySelector('#detail-name2').textContent = data.name;
        stock = document.querySelector('#detail-stock').textContent = data.stock;
        gender = document.querySelector('#detail-date').textContent = data.date_conquered;
        race = document.querySelector('#detail-profit').textContent = data.profit;
        specie = document.querySelector('#detail-buy').textContent = data.price_buy;
        date_nace = document.querySelector('#detail-sale').textContent = data.price_sale;
        date_up = document.querySelector('#detail-type').textContent = data.type_stock;
        date_up = document.querySelector('#detail-quantity').textContent = data.quantity;
        data.status = data.status
        $('#Modal_Detail').modal('show');

        /** DETAIL CLIENT EDIT */
        $('#Modal_Detail').on('click', 'a[rel="edit"]', function () {
        
            $('form')[0].reset();        
            modal_title.find('h5').html('Editar Producto');
            $('input[name="action"]').val('edit');
            $('input[name="id"]').val(data.id);
            $('input[name="name"]').val(data.name);
            $('input[name="stock"]').val(data.stock);
            $('input[name="price_buy"]').val(data.price_buy);
            $('input[name="price_sale"]').val(data.price_sale);
            $('input[name="profit"]').val(data.price_sale - data.price_buy);
    
            function cal_profit_product() {
                const precio_b = $('input[name="price_buy"]').val();
                const precio_v = $('input[name="price_sale"]').val();
                $('input[name="profit"]').val(precio_v - precio_b);
            };
    
            $('input[name="date_conquered"]').val(data.date_conquered);
            $('select[name="type_stock"]').val(data.type_stock);
            $('input[name="quantity"]').val(data.quantity);
            
            if (data.status == '<span class="badge badge-success btn-colores">Activado</span>') {
                input = document.querySelector('.status').setAttribute('checked','checked');
                
            }else{
                input = document.querySelector('.status').removeAttribute('checked','checked');
            };
    
            function type_unity() {
                option = $('select[name="type_stock"]').val();
                console.log(option);
                if ( option != 'cantidad' ) {
                    option = document.querySelector('#div-hidden').removeAttribute('hidden','hidden');
                }else{
                    option = document.querySelector('#div-hidden').setAttribute('hidden','hidden');
                };
            };
            
            $('#price_buy,#price_sale,#type_stock').change(function(){
                cal_profit_product()
                type_unity()
            });
    
            type_unity();

            $('#Modal_Detail').modal('hide');
            $('#ModalNew').modal('show');
        });

    });  

    /** DETAIL CLIENT DELETE */
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

    /** EDIT CLIENT */
    $('#data tbody').on('click', 'a[rel="edit"]', function () {
        $('form')[0].reset();        
        modal_title.find('h5').html('Editar Producto');
        var tr = tblCate.cell($(this).closest('td, li')).index();
        var data = tblCate.row(tr.row).data();
        $('input[name="action"]').val('edit');
        $('input[name="id"]').val(data.id);
        $('input[name="name"]').val(data.name);
        $('input[name="stock"]').val(data.stock);
        $('input[name="price_buy"]').val(data.price_buy);
        $('input[name="price_sale"]').val(data.price_sale);
        $('input[name="profit"]').val(data.price_sale - data.price_buy);

        function cal_profit_product() {
            const precio_b = $('input[name="price_buy"]').val();
            const precio_v = $('input[name="price_sale"]').val();
            $('input[name="profit"]').val(precio_v - precio_b);
        };

        $('input[name="date_conquered"]').val(data.date_conquered);
        $('select[name="type_stock"]').val(data.type_stock);
        $('input[name="quantity"]').val(data.quantity);
        
        if (data.status == '<span class="badge badge-success btn-colores">Activado</span>') {
            input = document.querySelector('.status').setAttribute('checked','checked');
            
        }else{
            input = document.querySelector('.status').removeAttribute('checked','checked');
        };

        function type_unity() {
            option = $('select[name="type_stock"]').val();
            console.log(option);
            if ( option != 'cantidad' ) {
                option = document.querySelector('#div-hidden').removeAttribute('hidden','hidden');
            }else{
                option = document.querySelector('#div-hidden').setAttribute('hidden','hidden');
            };
        };
        
        $('#price_buy,#price_sale,#type_stock').change(function(){
            cal_profit_product()
            type_unity()
        });

        type_unity();
        $('#ModalNew').modal('show');
    });

    /** DELETE CLIENT */
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
        placeholder: 'Selecionar Cliente',
        allowClear: true
        
    });
});

