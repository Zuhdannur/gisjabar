$(document).ready(function () {

    setTimeout(function(){
          $("#city").change()
     }, 300);

  var map = initMap();
  var dataContent = {};

  $('#filter').on('change', function() {

      $("#rth-desa").empty()
      $.ajax({
          method: "GET",
          url: this.value,
      }).done(function( data ) {
        var icon = L.icon({
            iconUrl: data.icon,
            iconSize:     [32, 32], // size of the icon
            shadowSize:   [50, 64], // size of the shadow
            iconAnchor:   [22, 94], // point of the icon which will correspond to marker's location
            shadowAnchor: [4, 62],  // the same for the shadow
            popupAnchor:  [-3, -76] // point from which the popup should open relative to the iconAnchor
        });

        L.marker(data.center, {icon: icon})
          .addTo(map)
          .bindPopup(JSON.stringify(data.attribute, null, ' ').replace(/[\{\}"\\]/g,''));

        map.flyTo(new L.LatLng(data.center[0], data.center[1]), 15, animate=true);
      });




  });

  $('#city').on('change', function() {
            var baseUrlDesa = $("#urls").val()
            var originalUrl = window.location.origin;

           var isAll = false
           if($("#city option:selected").text() == "-- SEMUA PETA KSK --") {
             isAll = true
           }
            $.ajax({
                method: "POST",
                headers: { "X-CSRFToken": getCookie("csrftoken") },
                url: baseUrlDesa,
                data: {
                    'city' : $(this).val(),
                    'isAll': isAll,
                    'kategori': $("#kategori-psu").val(),
                    'jenis': $("#jenis-psu").val(),
                    'csrfmiddlewaretoken': getCookie('csrftoken'),
                }
            }).done(function( data ) {

                clearlayers(map);

                if(isAll) {

                    $.each(data.data,function(index,value) {
                       new L.GeoJSON.AJAX(originalUrl+"/media/"+value.geojson, {
                            style: {
                                fillOpacity: .75,
                                color: value.attribute.color
                                }
                         }).addTo(map)
                        addIconToMapFromDetail(value.detail)
                    })

                 } else {
                 var geojsonLayer = new L.GeoJSON.AJAX(originalUrl+"/media/"+data.geojson, {
                    style: {
                        fillOpacity: .75,
                        color: data.attribute.color
                        }
                 })
                  geojsonLayer.addTo(map);
                  drawMap(map, geojsonLayer);
                  map.flyTo(new L.LatLng(data.center[0], data.center[1]), 12, animate=true);
                  addIconToMapFromDetail(data.detail)
                }


            });

//            $("#rth-desa").empty()
////            $("#rth-category").empty()
//
//            var selectedIndex = $("#city").prop('selectedIndex')
//
//            $("select#city_filter")[0].selectedIndex = selectedIndex;
//
//
//            var spiltsValus = $("#city_filter").val().split("/")
//            var id =  $("#city_filter").val()
//
//            var baseFilter = $("#urls").val()
//            var originalUrl = window.location.origin;
//
//            $.ajax({
//                method: "POST",
//                headers: { "X-CSRFToken": getCookie("csrftoken") },
//                url: baseFilter,
//                data: {
//                    'city' : id,
//                    'csrfmiddlewaretoken': getCookie('csrftoken'),
//                }
//            }).done(function( data ) {
//
//                clearlayers(map);
//
//                 var geojsonLayer = new L.GeoJSON.AJAX(originalUrl+"/media/"+data.city.geojson, {
//               style: {
//                    fillOpacity: .75
//                }
//          });
//
//          geojsonLayer.addTo(map);
//          drawMap(map, geojsonLayer);
//          map.flyTo(new L.LatLng(data.city.center[0], data.city.center[1]), 12, animate=true);
//
//                $("#rth-desa").empty()
//
//                $("#rth-desa").append('<option value="0">-- PILIH SEMUA DESA --</option>')
//               console.log(data['data'])
////                $("#rth-category").append('<option value="0">-- PILIH SEMUA KATEGORI --</option>')
//
//                var response = data['data']
//
//                setTimeout(function() {
//                    $.each(response,function(index,item) {
//                    $("#rth-desa").append('<option value='+ item.id +'>'+ item.attribute.nama +'</option>')
////                    $("#rth-category").append('<option value='+ item.id +'>'+ item.attribute.NamaPsu     +'</option>')
//
//                    new L.GeoJSON.AJAX(originalUrl+"/media/"+item.geojson, {
//                            style: {
//                                color: item.attribute.warna,
//                                 fillOpacity: .75
//                            }
//                    }).addTo(map);
//
//                    var textLatLng = [item.center[0], item.center[1]];
//                    var myTextLabel = L.marker(textLatLng, {
//                    icon: L.divIcon({
//                            className: 'text-labels',   // Set class for CSS styling
//                            html: item.attribute.nama
//                        }),
//                     zIndexOffset: 1000     // Make appear above other map features
//                    });
//
//                   myTextLabel.addTo(map)
//
//                    })
//                },300)
//
//            })

  });

  $("#rth-category").on('change',function() {
         var originalUrl = window.location.origin;

        if($(this).val() == 0) {
            $("#rth-desa").change()
        } else {
            $.ajax({
                method: "POST",
                headers: { "X-CSRFToken": getCookie("csrftoken") },
                url: $("#category-urls").val(),
                data: {
                    'desa' : $("#rth-desa").val(),
                    'rth-category': $("#rth-category").val(),
                    'csrfmiddlewaretoken': getCookie('csrftoken'),
                }
            }).done(function( data ) {

                var response = data['data']


                clearlayers(map);

        var geojsonLayer = new L.GeoJSON.AJAX(originalUrl+"/media/"+data.geojson, {
                style: {
                    color: data.attribute.warna,
                    fillOpacity: .75
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
                $.each(response , function(index,item) {
                    console.log(item)
                    var icon = L.icon({
                        iconUrl: originalUrl+"/media/"+item.attribute.icon,
                        iconSize:     [32, 32],
                        iconAnchor:   [20, 10]
                    });

                    var textLatLng = [item.center[0], item.center[1]];
                    var myTextLabel = L.marker(textLatLng, {
                        icon: L.divIcon({
                            className: 'text-labels',   // Set class for CSS styling
                            html: item.attribute.nama
                        }),
                    zIndexOffset: 1000     // Make appear above other map features
                    });


                    myTextLabel.addTo(map)
                    L.marker(item.center, {icon:icon})
                    .addTo(map)
                    .on({
                      click: function (e) {
                        $("#map-content").html("");
                        $("#map-content").html(makeTable(item.attribute));
                        $("#map-modal").modal("show");
                    }
                     });
                })
            })



        }


  })

//  $("#rth-desa, #rth-category").on('change',function() {
//              $( "#map-filter" ).submit();
//  })

  $( "#map-filter" ).submit(function( event ) {
    event.preventDefault();
    var form = $(this);
    var url = form.attr('action');

    $.ajax({
      method: "POST",
      url: url,
      data: form.serialize()
    }).done(function( data ) {
      if ( data['data'].length > 0 ) {
        var fdata = data['data'][0];
        var geojsonLayer = new L.GeoJSON.AJAX(fdata.geojson, {});
        geojsonLayer.addTo(map);
        drawMap(map, geojsonLayer);
        map.flyTo(new L.LatLng(fdata.center[0], fdata.center[1]), 12, animate=true);


//        profile_desa_rth_filter

      } else {

      }
      
      for (var d of data['data']) { 
        var icon = L.icon({
          iconUrl: d.icon,
          iconSize:     [32, 32], // size of the icon
          //shadowSize:   [50, 64], // size of the shadow
          iconAnchor:   [20, 10], // point of the icon which will correspond to marker's location
          //shadowAnchor: [4, 62],  // the same for the shadow
          //popupAnchor:  [-3, -76] // point from which the popup should open relative to the iconAnchor
        });

        dataContent[d.id] = makeTable(d.attribute)

        L.marker(d.center, {icon: icon, id: d.id})
          .addTo(map)
          .on({
            click: function (e) {
              $("#map-content").html("");
              $("#map-content").html(dataContent[e.target.options.id]);
              $("#map-modal").modal("show");
            }
          });
      }
    });


  });

  $("#rth-desa").on('change',function() {

        if($(this).val() == "0") {
            $( "#city" ).change();
            $("#rth-category").hide();
        } else {
            $("#rth-category").show();
      var originalUrl = window.location.origin;

      $.ajax({
          method: "GET",
          url: "/map/profile/city/rth/desa/"+this.value,
      }).done(function( data ) {
        clearlayers(map);

        var icon = L.icon({
            iconUrl: originalUrl+"/media/maps/icon/default.png",
            iconSize:     [32, 32], // size of the icon
            iconAnchor:   [20, 10], // point of the icon which will correspond to marker's location
            // shadowSize:   [50, 64], // size of the shadow
            // shadowAnchor: [4, 62],  // the same for the shadow
            // popupAnchor:  [-3, -76] // point from which the popup should open relative to the iconAnchor
          });

        var geojsonLayer = new L.GeoJSON.AJAX(originalUrl+"/media/"+data.geojson, {
                style: {
                    color: data.attribute.warna,
                    fillOpacity: .75
                }
          });

          geojsonLayer.addTo(map);
          drawMap(map, geojsonLayer);
//          map.flyTo(new L.LatLng(data.center[0], data.center[1]), 12, animate=true);

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

            $.ajax({
                method: "POST",
                headers: { "X-CSRFToken": getCookie("csrftoken") },
                url: $("#rth").val(),
                data: {
                    'rth-desa' : $("#rth-desa").val(),
                    'csrfmiddlewaretoken': getCookie('csrftoken'),
                }
            }).done(function( data ) {

               var response = data['data']
//               $("#rth-category").append('<option value="0">-- PILIH SEMUA KATEGORI --</option>')

               $.each(response, function(index,item) {
//                     $("#rth-category").append('<option value='+ item.id+'>'+ item.attribute.nama +'</option>')

                     var textLatLng = [item.center[0], item.center[1]];
                     var myTextLabel = L.marker(textLatLng, {
                            icon: L.divIcon({
                                className: 'text-labels',   // Set class for CSS styling
                                html: item.attribute.nama
                            }),
                        zIndexOffset: 1000     // Make appear above other map features
                        });

                  myTextLabel.addTo(map)
                   var icon = L.icon({
            iconUrl: originalUrl+"/media/"+item.attribute.icon,
            iconSize:     [32, 32], // size of the icon
            iconAnchor:   [20, 10], // point of the icon which will correspond to marker's location
            // shadowSize:   [50, 64], // size of the shadow
            // shadowAnchor: [4, 62],  // the same for the shadow
            // popupAnchor:  [-3, -76] // point from which the popup should open relative to the iconAnchor
          });

                  L.marker(item.center, {icon:icon})
            .       addTo(map)
            .on({
              click: function (e) {
                $("#map-content").html("");
                $("#map-content").html(makeTable(item.attribute));
                // $("#map-content").html(makeTable(data.attribute)+addPersentageAreaContainer());
                // var chart = persentageArea(data.area[0], data.area[1]);
                // chart.render();
                $("#map-modal").modal("show");
              }
            });

               })
            })
        })




      }
  })

  function addIconToMapFromDetail(data) {
    $.each(data,function(index,item){
     var originalUrl = window.location.origin;
                            var icon = L.icon({
                                iconUrl: originalUrl+"/media/"+item.icon,
                                iconSize:     [32, 32], // size of the icon
                                //shadowSize:   [50, 64], // size of the shadow
                                iconAnchor:   [20, 10], // point of the icon which will correspond to marker's location
                                //shadowAnchor: [4, 62],  // the same for the shadow
                                //popupAnchor:  [-3, -76] // point from which the popup should open relative to the iconAnchor
                            });

                        dataContent[item.id] = makeTable(item.attribute)

                        if($("#kategori-psu").val() == item.kategori || $("#jenis-psu").val() == item.jenis || $("#jenis-psu").val() == 0 || $("#kategori-psu").val() == 0) {
                         L.marker(item.center, {icon: icon, id: item.id})
                            .addTo(map)
                            .on({
                            click: function (e) {
                              $("#map-content").html("");
                              $("#map-content").html(dataContent[e.target.options.id]);
                              $("#map-modal").modal("show");
                            }
                          });
                        }


      })
}

  $("#kategori-psu").on('change',function(){
            $("#jenis-psu").empty()
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

                   $("#jenis-psu").append('<option value="'+ item.value +'">"'+ item.text +'"</option>')
                })
            })
        $("#city").change()
  })

  $("#jenis-psu").on('change',function(){
        $("#city").change()
  })

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

