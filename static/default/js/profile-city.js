$(document).ready(function () {


  var map = initMap();

  function addMarker(data) {
    var icon = L.icon({
      iconUrl: data.icon,
      iconSize:     [32, 32], // size of the icon
      iconAnchor:   [20, 10], // point of the icon which will correspond to marker's location
    });

    L.marker(data.center, {icon: icon})
      .addTo(map)
      .on({
        click: function (e) {
          $("#map-content").html("");
          $("#map-content").html(makeTable(data.attribute));
          // $("#map-content").html(makeTable(data.attribute)+addPersentageAreaContainer());
          // var chart = persentageArea(data.area[0], data.area[1]);
          // chart.render();
          $("#map-modal").modal("show");
        }
      }
    );
  }

  $('#filter').on('change', function() {

    $("#desa").empty()

    var url = $("#urls").val()
    var originalUrl = window.location.origin;
    var spiltsValus = $(this).val().split("/")
    var id = spiltsValus.pop();

  var myStyle = { // Define your style object
        "color": "#ff0000"
    };
    var myStyle2 = {
        "color": "#3279a8"
    }
    var styles = [myStyle,myStyle2]

      $.ajax({
          method: "GET",
          url: this.value,
      }).done(function( data ) {
        if (data.many) {
          clearlayers(map);
          var i = 0;
          for (var d of data['data']) {
            // var geojsonLayer = new L.GeoJSON.AJAX(d.geojson);
            new L.GeoJSON.AJAX(d.geojson , {
                style: styles[i]
            }).addTo(map);
            addMarker(d, d.area);
            i++
          }

          map.flyTo(new L.LatLng(-6.770070, 107.643271), 9, animate=true);
        } else {
          var icon = L.icon({
            iconUrl: data.icon,
            iconSize:     [32, 32], // size of the icon
            iconAnchor:   [20, 10], // point of the icon which will correspond to marker's location
            // shadowSize:   [50, 64], // size of the shadow
            // shadowAnchor: [4, 62],  // the same for the shadow
            // popupAnchor:  [-3, -76] // point from which the popup should open relative to the iconAnchor
          });

           var listedColor = []

          var geojsonLayer = new L.GeoJSON.AJAX(data.geojson, {
                style: myStyle
           // onEachFeature: function (f, l) {
           //   l.bindPopup('<pre>'+JSON.stringify(data.attribute, null, ' ').replace(/[\{\}"]/g,'')+'</pre>');
           //   // l.bindPopup(makeTable(data.attribute));
           // }
          });
          geojsonLayer.addTo(map);
          drawMap(map, geojsonLayer);
          map.flyTo(new L.LatLng(data.center[0], data.center[1]), 12, animate=true);

            $.ajax({
                method: "POST",
                headers: { "X-CSRFToken": getCookie("csrftoken") },
                url: url,
                data: {
                    'city' : id,
                    'csrfmiddlewaretoken': getCookie('csrftoken'),
                }
            }).done(function( data ) {

            $("#desa").empty()

            $("#desa").append('<option value="0">-- PILIH SEMUA DESA --</option>')
            var response = data['data']

            var index = 0

            var color  = []
            for (var i in response) {
            var d = response[index]
            var url = d.id

             $("#desa").append('<option value='  +url + '>'+ d.attribute.nama +'</option>')
            new L.GeoJSON.AJAX(originalUrl+"/media/"+d.geojson , {
                    style: {
                        color: d.attribute.warna
                    },
                    fillOpacity: 1
                }).addTo(map);
            var textLatLng = [d.center[0], d.center[1]];
            var myTextLabel = L.marker(textLatLng, {
                    icon: L.divIcon({
                    className: 'text-labels',   // Set class for CSS styling
                    html: d.attribute.nama
                    }),
                     zIndexOffset: 1000     // Make appear above other map features
                 });

            myTextLabel.addTo(map)
            index++
            }
        })

          L.marker(data.center, {icon: icon})
            .addTo(map)
            .on({
              click: function (e) {
                $("#map-content").html("");
                $("#map-content").html(makeTable(data.attribute));
                // $("#map-content").html(makeTable(data.attribute)+addPersentageAreaContainer());
                // var chart = persentageArea(data.area[0], data.area[1]);
                // chart.render();
                $("#map-modal").modal("show");
              }
            });
        }
      
      });
  
  });

  $("#desa").on('change',function() {

        if($("#desa").val() == "0") {
            $("#filter").change()
        }

      var originalUrl = window.location.origin;

      $.ajax({
          method: "GET",
          url: "/map/profile/city/desa/"+this.value,
      }).done(function( data ) {
            console.log(data)
           clearlayers(map);
           var icon = L.icon({
            iconUrl: originalUrl+"/media/maps/icon/default.png",
            iconSize:     [32, 32], // size of the icon
            iconAnchor:   [20, 10], // point of the icon which will correspond to marker's location
            // shadowSize:   [50, 64], // size of the shadow
            // shadowAnchor: [4, 62],  // the same for the shadow
            // popupAnchor:  [-3, -76] // point from which the popup should open relative to the iconAnchor
          });

           var listedColor = []

          var geojsonLayer = new L.GeoJSON.AJAX(originalUrl+"/media/"+data.geojson, {
                style: {
                    color: data.attribute.warna,
                    fillOpacity: 1
                }
          });

          geojsonLayer.addTo(map);
          drawMap(map, geojsonLayer);
          map.flyTo(new L.LatLng(data.center[0], data.center[1]), 12, animate=true);

           var textLatLng = [data.center[0], data.center[1]];
           var myTextLabel = L.marker(textLatLng, {
            icon: L.divIcon({
                className: 'text-labels',   // Set class for CSS styling
                html: data.attribute.nama
            }),
            zIndexOffset: 1000     // Make appear above other map features
           });

          myTextLabel.addTo(map)
          L.marker(data.center, {icon:icon})
            .addTo(map)
            .on({
              click: function (e) {
                $("#map-content").html("");
                $("#map-content").html(makeTable(data.attribute));
                // $("#map-content").html(makeTable(data.attribute)+addPersentageAreaContainer());
                // var chart = persentageArea(data.area[0], data.area[1]);
                // chart.render();
                $("#map-modal").modal("show");
              }
            });
      })


  })

  function getCookie(c_name)
{
    if (document.cookie.length > 0)
    {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1)
        {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start,c_end));
        }
    }
    return "";
 }

function getColor(desa , listedColor) {
    var text = desa.toUpperCase()
    $.each(listedColor, function (index,value) {
        console.log(value)
        if(text.toUpperCase() == value.name) {
            if(value.warna != "") {
                return value.warna
            }
        }
    })

    return ""
}

});

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
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
