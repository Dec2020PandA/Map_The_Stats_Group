const mapStyle = [
    {
        stylers: [{ visibility: "off" }],
    },
    {
        // featureType: "administrative.providence",
        // elementType: "labels.text.stroke",
        // stylers: [{ visibility: "off" }, { color: "#000000" }, {weight: 1}],
    },
    {
        featureType: "landscape",
        elementType: "geometry",
        stylers: [{ visibility: "off" }, { color: "#fcfcfc" }],
    },
    {
        featureType: "water",
        elementType: "geometry",
        stylers: [{ visibility: "on" }, { color: "#bfd4ff" }],
    },
];

var map;
function initMap() {
    startLoc = { lat: 40, lng: -100 };
    map = new google.maps.Map(document.getElementById("map"), {
        center: startLoc,
        zoom: 4,
        minZoom: 3,
        maxZoom: 17,
        disableDefaultUI: true,
        styles: mapStyle,
    });
    // set up the style rules and events for google.maps.Data
    loadMapShapes();

    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var state_data = JSON.parse(this.responseText);
        }
    }
    xmlhttp.open('GET', 'https://storage.googleapis.com/mapsdevsite/json/states.js', true)
    xmlhttp.send();

    map.data.setStyle({
        fillColor: 'blue',
        strokeWeight: 1
    })
    //LatLong click event
    let infoWindow = new google.maps.InfoWindow({
        content: "Click for Lat/Long",
        position: startLoc,
    })
    infoWindow.open(map);
    map.addListener("click", (mapsMouseEvent) => {
        infoWindow.close();
        infoWindow = new google.maps.InfoWindow({
            position: mapsMouseEvent.latLng,
        })
        infoWindow.setContent(
            JSON.stringify(mapsMouseEvent.latLng.toJSON(), null, 2)
        )
        infoWindow.open(map);
    })
    //click events
    map.data.addListener('mouseover', function (e) {
        map.data.overrideStyle(e.feature, { fillColor: 'yellow' });
    })
    map.data.addListener('click', function (e) {
        map.data.overrideStyle(e.feature, { fillColor: 'yellow' })
        var loc_id = e.feature.getProperty("STATE")
        var loc_name = e.feature.getProperty("NAME")
        var location = e.latLng;
        map.setCenter(location);
        map.setZoom(6);
        document.getElementById('hidden_location').value = loc_id;
        document.getElementById('hidden_name').value = loc_name;
    })
    map.data.addListener('mouseout', function (e) {
        map.data.overrideStyle(e.feature, { fillColor: 'blue' });
    })
}

/** Loads the state boundary polygons from a GeoJSON source. */
function loadMapShapes() {
    // load US state outline polygons from a GeoJson file
    map.data.loadGeoJson(
        "https://storage.googleapis.com/mapsdevsite/json/states.js",
        { idPropertyName: "STATE" }
    );
    // map.data.loadGeoJson(
    //     "https://storage.googleapis.com/map_the_stats/gz_2010_us_050_00_20m.js",
    //     { idPropertyName: "CENSUSAREA"}
    // )
}
