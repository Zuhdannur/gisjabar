function makeTable(mydata) {
  var table = $('<table border=1>');
  var tblHeader = "<tr>";
  for (var k in mydata[0]) tblHeader += "<th>" + k + "</th>";
  tblHeader += "</tr>";
  $(tblHeader).appendTo(table);
  $.each(mydata, function (index, value) {
    var TableRow = "<tr>";
    $.each(value, function (key, val) {
        TableRow += "<td>" + val + "</td>";
    });
    TableRow += "</tr>";
    $(table).append(TableRow);
  });
  console.log($(table).html);
  return $(table).html;
};

function drawMap(map, tile) {
  map.eachLayer(function (layer) {
    if (layer.options.id !== "mapbox.streets") {
      map.removeLayer(layer);
    }
  });
  map.addLayer(tile);
}

function initMap() {
  var map = L.map('map').setView([-6.881428, 107.682235], 9);
  L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
    maxZoom: 18,
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
      '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
      'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    id: 'mapbox.streets'
  }).addTo(map);

  return map;
}
