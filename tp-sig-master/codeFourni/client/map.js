var map = L.map('map').setView([45.15, 5.75], 13);

var highway = L.tileLayer.wms("http://localhost:4242/wms", {
    layers: 'highway',
    format: 'image/png',
    transparent: true
});

var building = L.tileLayer.wms("http://localhost:4242/wms", {
    layers: 'building',
    format: 'image/png',
    transparent: true
});

var CartoDB_Positron = L.tileLayer('http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png', {
	attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="http://cartodb.com/attributions">CartoDB</a>',
	subdomains: 'abcd',
	maxZoom: 19
});

var baseMaps = {"Fond de carte":  CartoDB_Positron};
map.addLayer(CartoDB_Positron);
var overlayMaps = {
    "autoroute":highway,
    "immeuble":building
};
L.control.layers(baseMaps, overlayMaps).addTo(map);
map.addLayer(highway);
map.addLayer(building);
