function message_error(obj) {
    let html = '';
    if(typeof (obj) === 'object'){
        $.each(obj, function (key,value) {
            html+=value
        })
    }
    else{
        html = obj
    }

    toastr.error(html)

}

/* Regresar a la pagina anterior */
function PagePrevious() {
    window.history.back();
}

function submit_detail(url, parameters, callback) {
    $.ajax({
        url: url, //window.location.pathname
        type: 'POST',
        data: parameters,
        dataType: 'json',
        processData: false,
        contentType: false,
    }).done(function (data) {
        if (!data.hasOwnProperty('error')) {
            callback(data);
            return false;
        }
        message_error(data.error);
    }).fail(function (jqXHR, textStatus, errorThrown) {
        alert(textStatus + ': ' + errorThrown);
    }).always(function (data) {

    });
}

/* jquery confirm para formularios */
function submit_with_ajax(url, title, content, parameters, callback) {
    $.confirm({
        theme: 'bootstrap',
        title: title,
        icon: 'fa fa-info',
        content: content,
        columnClass: 'small',
        typeAnimated: true,
        cancelButtonClass: 'btn-primary',
        draggable: true,
        dragWindowBorder: false,
        buttons: {
            info: {
                text: "Si",
                btnClass: 'btn-primary',
                action: function () {
                    $.ajax({
                        url: url, //window.location.pathname
                        type: 'POST',
                        data: parameters,
                        dataType: 'json',
                        processData: false,
                        contentType: false,
                    }).done(function (data) {
                        if (!data.hasOwnProperty('error')) {
                            callback();
                            return false;
                        }
                        message_error(data.error);
                    }).fail(function (jqXHR, textStatus, errorThrown) {
                        alert(textStatus + ': ' + errorThrown);
                    }).always(function (data) {

                    });
                }
            },
            danger: {
                text: "No",
                btnClass: 'btn-red',
                action: function () {

                }
            },
        }
    })
}


function submit_action(title, content, callback) {
    $.confirm({
        theme: 'bootstrap',
        title: title,
        icon: 'fa fa-info',
        content: content,
        columnClass: 'small',
        typeAnimated: true,
        cancelButtonClass: 'btn-primary',
        draggable: true,
        dragWindowBorder: false,
        buttons: {
            info: {
                text: "Si",
                btnClass: 'btn-primary',
                action: function () {
                    callback();
                }
            },
            danger: {
                text: "No",
                btnClass: 'btn-red',
                action: function () {

                }
            },
        }
    })
}

/**
$(function () {

    setInterval(function () {
        const DT = new Date();
            hours = DT.getHours();
            minutes = DT.getMinutes();
            seconds = DT.getSeconds();
            ampm = '';

            // VALIDATE TYPE TIME
            if (hours >= 12) {
                ampm = 'PM';
            }else{
                ampm = 'AM';
            };
            if (hours == 0)  {
                hours = 12;
            };
            // VALIDATE 0 
            if (hours < 10) {
                hours = '0' + hours
            };
            if (minutes < 10) {
                minutes = '0' + minutes;
            };
            if (seconds < 10) {
                seconds = '0' + seconds;
            };

            time = hours + ':' + minutes + ':' + seconds +  ' ' + ampm; 
        const Hora = document.getElementById('hora-menu').innerHTML = time;

        const day_week = DT.getDay();
            day = DT.getDate();
            month = DT.getMonth();
            year = DT.getFullYear();
        var day_list = ['Domingo','Lunes','Martes','Miercoles','Jueves','Viernes','Sabado'];
        var month_list = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'];
        const get_day_list = day_list[day_week];
        const get_month_list = month_list[month];
        const Fecha = document.getElementById('date-menu').innerHTML = get_day_list + ' ' + day + ' de ' + get_month_list + ' del ' + year;

    },1000);
});
*/