$(document).ready(function () {

  var map = initMap();

  $('#filter').on('change', function() {
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
          .bindPopup('<pre>'+JSON.stringify(data.attribute, null, ' ').replace(/[\{\}"]/g,'')+'</pre>');

        map.flyTo(new L.LatLng(data.center[0], data.center[1]), 13, animate=true);
      });
  });

});
