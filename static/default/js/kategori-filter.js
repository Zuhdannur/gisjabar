
$(document).ready(function(){
    var $ = django.jQuery;

    $("#id_kategori_psu").on('change',function(){
        $("#id_jenis_psu").empty()
        var originalUrl = window.location.origin+"/filter-kategori";
        $.ajax({
                method: "POST",
                headers: { "X-CSRFToken": getCookie("csrftoken") },
                headers: { "X-CSRFToken": getCookie("csrftoken") },
                url: originalUrl,
                data: {
                    'id': $(this).val(),
                    'csrfmiddlewaretoken': getCookie('csrftoken'),
                }
            }).done(function( data ) {
                $.each(data['data'] , function(index,item) {
                    console.log(item)
                   $("#id_jenis_psu").append('<option value="'+ item.value +'">"'+ item.text +'"</option>')
                })
            })
    })
});

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i];
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});