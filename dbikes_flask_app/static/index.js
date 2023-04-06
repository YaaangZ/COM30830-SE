
function addMarkers(stations){
  stations.forEach(station =>{
    const lat = Number(station.position_lat)
    const lng = Number(station.position_lng)
    const infoString = `<h1 style="text-align: center; font-size:25px; "> Station Name: ${station.address} <h1>
    <p style="font-size:20px"> 
    <i class="fa-sharp fa-solid fa-square-parking"></i>
    Available Bikes Stand: ${station.available_bike_stands} 
    </p>
    <p style="font-size:20px">
    <i class="fa-solid fa-person-biking"></i>
    Available Bikes: ${station.available_bikes} 
    </p>`;

    let markerIcon;

    if (station.available_bikes >= 25) {
      markerIcon = {
        url: document.getElementById('my-element-1').dataset.imageUrl,
      }
    } else if (station.available_bikes >= 10 && station.available_bikes <=24) {
      markerIcon = {
        url: document.getElementById('my-element-2').dataset.imageUrl,
      }
    } else if (station.available_bikes <= 9) {
      markerIcon = {
        url: document.getElementById('my-element-3').dataset.imageUrl,
      }
    } 
    var marker = new google.maps.Marker({
        position: {
         lat: lat,
         lng: lng,  
        },
        map: map,
        icon: markerIcon,
        title: station.name,
        station_number: station.number,
        animation: google.maps.Animation.DROP // Add animation property

      });


      google.maps.event.addListener(map, 'zoom_changed', function() {
        var pixelSizeAtZoom0 = 50; //the size of the icon at zoom level 0
        var maxPixelSize = 50; //restricts the maximum size of the icon, otherwise the browser will choke at higher zoom levels trying to scale an image to millions of pixels
            
        var zoom = map.getZoom();
        var relativePixelSize = Math.round(pixelSizeAtZoom0*Math.pow(2,zoom)); // use 2 to the power of current zoom to calculate relative pixel size.  Base of exponent is 2 because relative size should double every time you zoom in
        
        if(relativePixelSize > maxPixelSize) //restrict the maximum size of the icon
            relativePixelSize = maxPixelSize;
        
        //change the size of the icon
        marker.setIcon(
            new google.maps.MarkerImage(
                marker.getIcon().url, //marker's same icon graphic
                null,//size
                null,//origin
                null, //anchor
                new google.maps.Size(relativePixelSize, relativePixelSize) //changes the scale
            )
        );        
    });

    const infowindow = new google.maps.InfoWindow({  
      content: infoString
    });

    marker.addListener('mouseover', function(){
      infowindow.open(map, marker);
      marker.setAnimation(google.maps.Animation.BOUNCE);
    });

    marker.addListener('mouseout', function() {
      infowindow.close();
      marker.setAnimation(null);

    });

    marker.addListener('click', createRoute())
 });
}

function createRoute(){
  
}
function getStations(){

    fetch("/stations")
      .then((response)=> response.json())
      .then((data) => {
      console.log(data);
      // console.log("fetch response", typeof 
      // data)   
      addMarkers(data);
      });
      
}


// function clickEvent(id){

// }

// function showStaticData(id){


// }



function initMap() {
    // The location of Dublin
    const dublinLatLng = { lat: 53.350140, lng: -6.266155};


    // The map, centered at Dublin
    map = new google.maps.Map(document.getElementById("map"),{
      zoom: 15,
      center: dublinLatLng,

    });
    map.setOptions({styles: styles['hide']});
 

    getStations();
    new AutocompleteDirectionsHandler(map);

  }

     
  const styles = {
    hide: [
    {
      featureType: "poi.business",
      stylers: [{ visibility: "off" }],
    },
    {
      featureType: "transit",
      elementType: "labels.icon",
      stylers: [{ visibility: "off" }],
    },
      
  ]
  }
// google api functionality 
  class AutocompleteDirectionsHandler {
    map;
    originPlaceId;
    destinationPlaceId;
    travelMode;
    directionsService;
    directionsRenderer;
    constructor(map) {
      this.map = map;
      this.originPlaceId = "";
      this.destinationPlaceId = "";
      this.travelMode = google.maps.TravelMode.WALKING;
      this.directionsService = new google.maps.DirectionsService();
      this.directionsRenderer = new google.maps.DirectionsRenderer({
        polylineOptions: {
          strokeColor: "black",
        },
      });
      this.directionsRenderer.setMap(map);


    const originInput = document.getElementById("journeyfrom");
    const destinationInput = document.getElementById("journeyto");
    const modeSelector = document.getElementById("mode-selector");
    // Specify just the place data fields that you need.
    const originAutocomplete = new google.maps.places.Autocomplete(
      originInput,
      { fields: ["place_id"] }
    );
    // Specify just the place data fields that you need.
    const destinationAutocomplete = new google.maps.places.Autocomplete(
      destinationInput,
      { fields: ["place_id"] }

    );


    this.setupClickListener(
      "changemode-walking",
      google.maps.TravelMode.WALKING
    );
    this.setupClickListener(
      "changemode-transit",
      google.maps.TravelMode.TRANSIT
    );
    this.setupClickListener(
      "changemode-driving",
      google.maps.TravelMode.DRIVING
    );


    this.setupPlaceChangedListener(originAutocomplete, "ORIG");
    this.setupPlaceChangedListener(destinationAutocomplete, "DEST");
  }
  // Sets a listener on a radio button to change the filter type on Places
  // Autocomplete.
  setupClickListener(id, mode) {
    const radioButton = document.getElementById(id);

    radioButton.addEventListener("click", () => {
      this.travelMode = mode;
      this.route();
    });
  }
  setupPlaceChangedListener(autocomplete, mode) {
    autocomplete.bindTo("bounds", this.map);
    autocomplete.addListener("place_changed", () => {
      const place = autocomplete.getPlace();

      if (!place.place_id) {
        window.alert("Please select an option from the dropdown list.");
        return;
      }

      if (mode === "ORIG") {
        this.originPlaceId = place.place_id;
      } else {
        this.destinationPlaceId = place.place_id;
      }

      this.route();
    });
  }
  route() {
    if (!this.originPlaceId || !this.destinationPlaceId) {
      return;
    }

    const me = this;

    this.directionsService.route(
      {
        origin: { placeId: this.originPlaceId },
        destination: { placeId: this.destinationPlaceId },
        travelMode: this.travelMode,
      },
      (response, status) => {
        if (status === "OK") {
          me.directionsRenderer.setDirections(response);
        } else {
          window.alert("Directions request failed due to " + status);
        }
      }

  
    );
    }

    // event listener to click for and create a route for when marker is clicked 


}
// generating a filter that calculates the closest marker to the origin and the destination






  

  function openNav() {
    document.getElementById("main").style.marginLeft = "25%";
    document.getElementById("mySidebar").style.width = "25%";
    document.getElementById("mySidebar").style.display = "block";
    document.getElementById("openNav").style.display = 'none';
  }
  function closeNav() {
    document.getElementById("main").style.marginLeft = "0%";
    document.getElementById("mySidebar").style.display = "none";
    document.getElementById("openNav").style.display = "inline-block";
  }

var map = null;
window.initMap = initMap;

