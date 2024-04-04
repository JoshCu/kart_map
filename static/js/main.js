// Initialize the map
var map = L.map('map').setView([40, -96], 5);

// Add OpenStreetMap tiles to the map
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxNativeZoom: 19,
    maxZoom: 25,
    crs: L.CRS.EPSG3857
}).addTo(map);


function loadAndDisplayGeoJson(filename) {
    $.getJSON(`/process-file/${filename}`, function (data) {
        var color = getRandomColor();
        var geoJsonLayer = L.geoJSON(data, {
            style: function (feature) {

                return { color: color };
            }
        }).addTo(map).bindPopup(filename);
        addLegend(filename, color);

        var bounds = geoJsonLayer.getBounds();
        map.fitBounds(bounds);
    }).fail(function () {
        console.error("Failed to load GeoJSON data for " + filename);
    });
}

function addLegend(filename, color) {
    var legend = L.control({ position: 'bottomright' });
    legend.onAdd = function (map) {
        var div = L.DomUtil.create('div', 'info legend');
        div.innerHTML += `<span style="color:${color}">${filename}</span><br>`;
        return div;
    };
    legend.addTo(map);
}

function getRandomColor() {
    var letters = '0123456789ABCDEF';
    var color = '#';
    for (var i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}
// Get the list of files and display them
$.getJSON('/list-files', function (filenames) {
    filenames.forEach(function (filename) {
        loadAndDisplayGeoJson(filename);
    });
});