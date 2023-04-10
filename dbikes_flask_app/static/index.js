var directionsService;

var directionsRenderer;

let lastClickedMarker = null;

let currentRoute

function initMap() {

  directionsService = new google.maps.DirectionsService();
  directionsRenderer = new google.maps.DirectionsRenderer();

  // The location of Dublin
  const dublinLatLng = { lat: 53.350140, lng: -6.266155};

  // The map, centered at Dublin
  map = new google.maps.Map(document.getElementById("map"),{
    zoom: 15,
    center: dublinLatLng,

  });
  map.setOptions({styles: styles['hide']});
  getStations();
  getWeather();

  directionsRenderer.setMap(map); // add the renderer to the map

  // new AutocompleteDirectionsHandler(map);

}


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
    document.getElementById('availablebike-button').addEventListener('click', function(){
      console.log('hi')
    if (station.available_bikes >= 25) {
      marker.setIcon({
        url: document.getElementById('my-element-1').dataset.imageUrl,
      })
    } else if (station.available_bikes >= 10 && station.available_bikes <=24) {
      marker.setIcon({
        url: document.getElementById('my-element-2').dataset.imageUrl,
      })
    } else if (station.available_bikes <= 9) {
      marker.setIcon({
        url: document.getElementById('my-element-3').dataset.imageUrl,
      })
    } 
  })


  document.getElementById('availablebikestand-button').addEventListener('click', function(){
    console.log('hi')
  if (station.available_bike_stands >= 25) {
    marker.setIcon({
      url: document.getElementById('my-element-1').dataset.imageUrl,
    })
  } else if (station.available_bike_stands >= 10 && station.available_bikes <=24) {
    marker.setIcon({
      url: document.getElementById('my-element-2').dataset.imageUrl,
    })
  } else if (station.available_bike_stands <= 9) {
    marker.setIcon({
      url: document.getElementById('my-element-3').dataset.imageUrl,
    })
  } 
})
    var marker = new google.maps.Marker({
        position: {
         lat: lat,
         lng: lng,  
        },
        map: map,
        icon: markerIcon,
        title: station.name,
        address: station.address,
        position_lat: station.position_lat,
        position_lng: station.position_lat,
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
    marker.addListener('click', () => {

      // If this is the first marker clicked, fill in the "from" field
      if (!lastClickedMarker) {
        document.getElementById('journeyfrom').value = marker.address;
        lastClickedMarker = marker;
      } else {
        // Otherwise, fill in the "to" field and create a route
    
        const from = lastClickedMarker.getPosition();
        const to = marker.getPosition();
        const request = {
          origin: from,
          destination: to,
          travelMode: 'WALKING',
        };

            // Clear any existing route
    if (currentRoute) {
      currentRoute.setMap(null);
    }
   
        directionsService.route(request, function(result, status) {
            if (status === 'OK') {
              // Route was successfully calculated
              directionsRenderer.setDirections(result);
              openNav()

            } else if (status === 'ZERO_RESULTS') {
              // No route could be found between the origin and destination
              console.log('No route found.');
            } else if (status === 'INVALID_REQUEST') {
              // Request was missing required parameters
              console.log('Invalid request.');
            } else if (status === 'OVER_QUERY_LIMIT') {
              // Request exceeded the usage limits for the API
              console.log('API usage limit exceeded.');
            } else if (status === 'REQUEST_DENIED') {
              // Request was denied, possibly due to missing or invalid API key
              console.log('Request denied.');
            } else if (status === 'UNKNOWN_ERROR') {
              // An unknown error occurred
              console.log('Unknown error.');
            }
          });
                
        document.getElementById('journeyto').value = marker.address;
        lastClickedMarker = null;
      }
    });
  });
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
  // class AutocompleteDirectionsHandler {
  //   map;
  //   originPlaceId;
  //   destinationPlaceId;
  //   travelMode;
  //   directionsService;
  //   directionsRenderer;
  //   constructor(map) {
  //     this.map = map;
  //     this.originPlaceId = "";
  //     this.destinationPlaceId = "";
  //     this.travelMode = google.maps.TravelMode.WALKING;
  //     this.directionsService = new google.maps.DirectionsService();
  //     this.directionsRenderer = new google.maps.DirectionsRenderer({
  //       polylineOptions: {
  //         strokeColor: "black",
  //       },
  //     });
  //     this.directionsRenderer.setMap(map);


  //   const originInput = document.getElementById("journeyfrom");
  //   const destinationInput = document.getElementById("journeyto");
  //   const modeSelector = document.getElementById("mode-selector");
  //   // Specify just the place data fields that you need.
  //   const originAutocomplete = new google.maps.places.Autocomplete(
  //     originInput,
  //     { fields: ["place_id"] }
  //   );
  //   // Specify just the place data fields that you need.
  //   const destinationAutocomplete = new google.maps.places.Autocomplete(
  //     destinationInput,
  //     { fields: ["place_id"] }

  //   );


  //   this.setupClickListener(
  //     "changemode-walking",
  //     google.maps.TravelMode.WALKING
  //   );
  //   this.setupClickListener(
  //     "changemode-transit",
  //     google.maps.TravelMode.TRANSIT
  //   );
  //   this.setupClickListener(
  //     "changemode-driving",
  //     google.maps.TravelMode.DRIVING
  //   );


  //   this.setupPlaceChangedListener(originAutocomplete, "ORIG");
  //   this.setupPlaceChangedListener(destinationAutocomplete, "DEST");
  // }
  // // Sets a listener on a radio button to change the filter type on Places
  // // Autocomplete.
  // setupClickListener(id, mode) {
  //   const radioButton = document.getElementById(id);

  //   radioButton.addEventListener("click", () => {
  //     this.travelMode = mode;
  //     this.route();
  //   });
  // }
  // setupPlaceChangedListener(autocomplete, mode) {
  //   autocomplete.bindTo("bounds", this.map);
  //   autocomplete.addListener("place_changed", () => {
  //     const place = autocomplete.getPlace();

  //     if (!place.place_id) {
  //       window.alert("Please select an option from the dropdown list.");
  //       return;
  //     }

  //     if (mode === "ORIG") {
  //       this.originPlaceId = place.place_id;
  //     } else {
  //       this.destinationPlaceId = place.place_id;
  //     }

  //     this.route();
  //   });
  // }
  // route() {
  //   if (!this.originPlaceId || !this.destinationPlaceId) {
  //     return;
  //   }

  //   const me = this;

  //   this.directionsService.route(
  //     {
  //       origin: { placeId: this.originPlaceId },
  //       destination: { placeId: this.destinationPlaceId },
  //       travelMode: this.travelMode,
  //     },
  //     (response, status) => {
  //       if (status === "OK") {
  //         me.directionsRenderer.setDirections(response);
  //       } else {
  //         window.alert("Directions request failed due to " + status);
  //       }
  //     }

  
  //   );
  //   }



  // <!--This part is displayed weather information vertically-->
  function getWeather() {
    fetch(`https://api.openweathermap.org/data/2.5/forecast?lat=53.3498006&lon=-6.2602964&units=metric&appid=8f2e40db6b1c4dcc89b68735362dbc56`)
      .then(response => response.json())
      .then(data => {
        const forecast = data.list;
        const currentTemp = data.list[0].main.temp;
        const currentWeatherMain = data.list[0].weather[0].main;
        const currentWeatherIcon = data.list[0].weather[0].icon;
  
        // code to display current weather data
        const weatherDiv = document.getElementById("weather");
        weatherDiv.classList.add("animated-bg");
  
        // Add weather condition class to the weather div
        if (currentWeatherMain.includes('Cloud')) {
          weatherDiv.classList.add('cloudy');
        } else if (currentWeatherMain.includes('Rain')) {
          weatherDiv.classList.add('rainy');
        } else if (currentWeatherMain.includes('Snow')) {
          weatherDiv.classList.add('snowy');
        } else if (currentWeatherMain.includes('Clear')) {
          weatherDiv.classList.add('sunny');
        }
  
        weatherDiv.innerHTML = `
          <div class="weather-border">
            <div class="weather-header">Current Weather</div>
            <div class="weather-content">
              <img src="https://openweathermap.org/img/wn/${currentWeatherIcon}@2x.png" alt="${currentWeatherMain}" class="icon">
              ${currentTemp} &#8451;, ${currentWeatherMain}
            </div>
          </div>
          <div class="dropdown">
            <button class="dropbtn">Few Hours Forecast</button>
            <div class="dropdown-content">
              ${forecast.slice(0, 6).map((data) => {
                const time = new Date(data.dt * 1000).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
                const temp = data.main.temp;
                const weatherMain = data.weather[0].main;
                const weatherIcon = data.weather[0].icon;
                return `
                  <div style="font-size: 20px;" class="weather-content">
                    <div>${time}</div>
                    <img src="https://openweathermap.org/img/wn/${weatherIcon}.png" alt="${weatherMain}">
                    <div>${temp} &#8451;, ${weatherMain}</div>
                  </div>
                `;
              }).join('')}
            </div>
          </div>
          <!--  More details part-->
          <div class="dropdown">
            <button class="dropbtn">Current Weather More Details</button>
              <div class="dropdown-content">
                <a href="#">Temperature: ${currentTemp} &#8451;</a>
                <a href="#" class="details">Feels Like: ${forecast[0].main.feels_like} &#8451;</a>
                <a href="#" class="details">Humidity: ${forecast[0].main.humidity}%</a>
                <a href="#" class="details">Wind Direction: ${forecast[0].wind.deg} deg</a>
                <a href="#" class="details">Wind Speed: ${forecast[0].wind.speed} m/s</a>
              </div>
            </div>
          <!-- 5-day forecast-->
          <div class="dropdown">
            <button class="dropbtn">5-Day Forecast</button>
            <div class="dropdown-content five-day">
              ${forecast.map((data, index) => {
                if (index % 8 === 0) {
                  const date = new Date(data.dt_txt).toLocaleDateString();
                  const temp = data.main.temp;
                  const weatherMain = data.weather[0].main;
                  const weatherIcon = data.weather[0].icon;
                  return `
                    <a href="#" class = "weather-date">${date}</a>
                    <div class="weather-content">
                      <img src="https://openweathermap.org/img/wn/${weatherIcon}.png" alt="${weatherMain}">
                      <a href="#" class="details">Temperature: ${temp} &#8451;</a>
                      <a href="#" class="details">Weather: ${weatherMain}</a>
                    </div>
                  `;
                }
              }).join('')}
            </div>
          </div>`;
        const dropdowns = document.querySelectorAll(".dropdown");
        const details = document.querySelectorAll(".details");
  
        dropdowns.forEach(dropdown => {
          dropdown.addEventListener("click", function() {
            this.nextElementSibling.classList.toggle("show");
          });
        });
  
        details.forEach(detail => {
          detail.addEventListener("click", function(event) {
            event.stopPropagation();
          });
        });
  
        window.onclick = function(event) {
          if (!event.target.matches('.dropbtn')) {
            const dropdownContent = document.querySelectorAll(".dropdown-content");
            dropdownContent.forEach(content => {
              if (content.classList.contains('show')) {
                content.classList.remove('show');
              }
            });
          }
        };
      });
  }
  

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

