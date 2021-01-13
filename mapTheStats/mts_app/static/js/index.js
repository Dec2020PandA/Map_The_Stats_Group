window.us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'American Samoa': 'AS',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Guam': 'GU',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands':'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
}


console.log("Loaded all those states!")

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

    var msahttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
             window.msa_data = JSON.parse(this.responseText);
        }
    }
    xmlhttp.open('GET', 'https://cors-anywhere.herokuapp.com/https://storage.googleapis.com/map_the_stats/msa_data_usa.json', true)
    xmlhttp.send();

    map.data.setStyle({
        fillColor: '#2195bc',
        strokeColor: 'white',
        strokeWeight: 1
    })
    // //LatLong click event
    // let infoWindow = new google.maps.InfoWindow({
    //     content: "Click for Lat/Long",
    //     position: startLoc,
    // })
    // infoWindow.open(map);
    // map.addListener("click", (mapsMouseEvent) => {
    //     infoWindow.close();
    //     infoWindow = new google.maps.InfoWindow({
    //         position: mapsMouseEvent.latLng,
    //     })
    //     infoWindow.setContent(
    //         JSON.stringify(mapsMouseEvent.latLng.toJSON(), null, 2),
    //     )
    //     infoWindow.open(map);
    // })
    //click events
    map.data.addListener('mouseover', function (e) {
        map.data.overrideStyle(e.feature, { fillColor: 'yellow', strokeWeight: 3 });
    })
    map.data.addListener('click', function (e) {
        // load geo json MSA data
        var msa_map = map.data.loadGeoJson(
            'https://cors-anywhere.herokuapp.com/https://storage.googleapis.com/map_the_stats/msa_data_usa.json',
        )
        map.data.overrideStyle(e.feature, { fillColor: 'yellow' })
        var loc_id = e.feature.getProperty("STATE")
        var loc_name = e.feature.getProperty("NAME")
        var location = e.latLng;
        map.setCenter(location);
        map.setZoom(6);
        console.log(JSON.stringify(location))
            // var lon_lat = JSON.stringify({location})
            // for(key in lon_lat) {
            //     console.log(key)
            // }
        // new_data = JSON.stringify(location[lat])+"," + JSON.stringify(location[lng])
        // console.log(new_data)
        document.getElementById('selected_area').value = location;
        document.getElementById('hidden_location').value = loc_id;
        document.getElementById('hidden_name').value = loc_name;

        // function to find the state name from the 
        
        for(var key in us_state_abbrev) {
            if(key == loc_name)
            var msa_fetcher = us_state_abbrev[key]
            console.log(msa_fetcher)
        }

        // function to reveal MSA data on state click
        var x = msa_data;
        for(key in x) {
            if (key == 'features') {
                var arr = x[key];
                for(var i = 0; i < arr.length; i++) {
                    for(new_key in arr[i]) {
                        if(new_key == 'properties'){
                            var properties = arr[i][new_key]
                            for(another_key in properties){
                                if(another_key == 'NAME'){
                                    var msa_chex = properties[another_key].indexOf(msa_fetcher)
                                    if(msa_chex > -1){
                                        console.log(properties[another_key] + " " + "Succesfully determined to be in the selected state!")
                                        console.log(msa_map)
                                    }
                                }
                            }
                        }
                    }
                }     
            }
        }  

    })
    map.data.addListener('mouseout', function (e) {
        map.data.overrideStyle(e.feature, { fillColor: '#2195bc', strokeWeight: 1 });
    })

    }

    /** Loads the state boundary polygons from a GeoJSON source. */

    function loadMapShapes() {
    // load US state outline polygons from a GeoJson file
    map.data.loadGeoJson(
        "https://storage.googleapis.com/mapsdevsite/json/states.js",
        { idPropertyName: "STATE" },  
    )
    map.data.loadGeoJson(
        'https://cors-anywhere.herokuapp.com/https://storage.googleapis.com/map_the_stats/us_outline.json',
    )
}
