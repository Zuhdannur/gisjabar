$(document).ready(function () {

  var map = initMap();

  $('#filter').on('change', function() {
      $.ajax({
          method: "GET",
          url: this.value,
      }).done(function( data ) {
        console.log( data );
        var geojsonLayer = new L.GeoJSON.AJAX(data.geojson, {
         onEachFeature: function (f, l) {
           l.bindPopup('<pre>'+JSON.stringify(data.attribute, null, ' ').replace(/[\{\}"]/g,'')+'</pre>');
           // l.bindPopup(makeTable(data.attribute));
         }
        });
        // geojsonLayer.addTo(map);

        drawMap(map, geojsonLayer);
        map.flyTo(new L.LatLng(data.center[0], data.center[1]), 12, animate=true);
      });
  });

});
