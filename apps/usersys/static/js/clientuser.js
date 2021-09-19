
$(function () {
    console.log('gooa')
    gender = document.querySelector('#detail-gender').innerHTML;
    if (gender == 'Femenino'){
        img = document.querySelector('#detail-img').setAttribute("src","/static/img/avatar2.png");
        img = document.querySelector('#detail-img2').setAttribute("src","/static/img/avatar2.png");

    }else{
        img = document.querySelector('#detail-img').setAttribute("src","/static/img/avatar5.png");
        img = document.querySelector('#detail-img2').setAttribute("src","/static/img/avatar5.png");
    } 
});
/**
$(function () {
    $.ajax({
        url: window.location.pathname,
        type: 'GET',
        dataType:'json',
        success: function(data) {
            console.log(data)
        },
        failure: function(data) { 
            alert('Got an error dude');
        }
    }); 
});
**/



