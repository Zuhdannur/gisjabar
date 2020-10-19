function stakedBar(n1, n2) {
  var s = '<h3>Perbandingan Luas Wilayah dengan RTH</h3>';
  s += '<div class="stacked-bar-graph">';
  if (n1 > 0) {
    s += '<span style="width:' + n1 + '%" class="bar-1 span-bar"> LUAS RTH: ' + n1 + '%</span>';
  }
  s += '<span style="width:' + n2 + '%" class="bar-2 span-bar"> LUAS WILAYAH: ' + n2 + '%</span>';
  s += '</div>';

  return s;
}

function addPersentageAreaContainer() {
  return '<div id="chartContainer" style="height: 250px; width: 100%;" align="right"></div>';
}

function persentageArea(n1, n2) {
  var chart = new CanvasJS.Chart("chartContainer",
  {
    height: 260,
    title:{
      text: "Prosentase RTR = sekian prosen Dari Luas wilayah",
      fontFamily: "Impact",
      fontWeight: "normal"
    },

    legend:{
      verticalAlign: "bottom",
      horizontalAlign: "center"
    },
    data: [
      {
        //startAngle: 45,
        indexLabelFontSize: 18,
        indexLabelFontFamily: "Garamond",
        indexLabelFontColor: "darkgrey",
        indexLabelLineColor: "darkgrey",
        indexLabelPlacement: "outside",
        type: "doughnut",
        showInLegend: true,
        dataPoints: [
          {  y: n1, legendText:"Luas RTH " + n1 + "%", indexLabel: "Luas RTH " + n1 + "%" },
          {  y: n2, legendText:"Luas Wilayah " + n2 + "%", indexLabel: "Luas Wilayah " + n2 + "%" },
        ]
     }
    ]
  });
  return chart;
}

function makeTable(data) {
  var table = '<table class="table table-striped">';
  
  var TableRow = '';
  $.each(data, function (index, value) {
    TableRow += "<tr>";
    TableRow += "<th>" + index + "</th>";
    TableRow += "<td>" + value + "</td>";
    TableRow += "</tr>";
  });
  
  table += TableRow;
  table += '</table>';
  
  return table;
};

function clearlayers(map) {
  map.eachLayer(function (layer) {
    if (layer.options.id !== "mapbox.streets") {
      map.removeLayer(layer);
    }
  });
}

function drawMap(map, tile) {
  clearlayers(map);
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
