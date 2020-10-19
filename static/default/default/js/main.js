$(document).ready(function () {

  var map = L.map('map').setView([-6.881428, 107.682235], 9);
  L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
    maxZoom: 18,
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
      '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
      'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    id: 'mapbox.streets'
  }).addTo(map);

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
