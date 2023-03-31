
function addMarkers(stations){
  stations.forEach(station =>{
    const lat = Number(station.position_lat)
    const lng = Number(station.position_lng)
    const infoString = `<h6 style="text-align: center; font-size:15px; "> Station Information <h6>
    <ul style="font-size:15px">
    <li> Station Number: ${station.number} </li>
    <li> Station Address: ${station.address} </li>
    <i class="fa-sharp fa-solid fa-square-parking"></i>
    <li> Available Bikes Stand: ${station.available_bike_stands} </li>
    <li> Available Bikes: ${station.available_bikes} </li>
    </ul>`;

    let markerIcon;

    if (station.available_bikes >= 25) {
      markerIcon = {
        url: document.getElementById('my-element').dataset.imageUrl,
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

