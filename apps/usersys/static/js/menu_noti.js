$(function () {
    $('a[rel="active"]').on('click', function () {
        var parameters = new FormData();
        parameters.append('action', 'active')
        submit_with_ajax(window.location.pathname,'Notifiación', '¿Estas seguro de cambiar el estado de las notificaciones?', parameters, function () {
            
            window.location.replace('/auth/menu_noficaciones/');
            
        });

    });


    $('a[rel="inactive"]').on('click', function () {
        var parameters = new FormData();
        parameters.append('action', 'inactive')
        submit_with_ajax(window.location.pathname,'Notifiación', '¿Estas seguro de cambiar el estado de las notificaciones?', parameters, function () {
            
            window.location.replace('/auth/menu_noficaciones/');
            
        });

    });
});
