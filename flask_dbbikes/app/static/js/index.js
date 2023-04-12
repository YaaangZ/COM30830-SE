// define the global variables
let map = null;
const iconImage = "../img/bikeIcon.png";//24px
let infowindow;
let focus;
let currentStation;
let sideBarOpened = false;

// Load the Google Charts library
google.charts.load('current', {'packages':['corechart']});
function initMap() {
    const dublin = {lat: 53.350140, lng: -6.266155};
    const mapProp= {center: dublin, zoom:14};
    const styles = {
        hide: [
            {
                featureType: "poi.business",
                stylers: [{ visibility: "off" }],},
            {
                featureType: "transit",
                elementType: "labels.icon",
                stylers: [{ visibility: "off" }],
            },
            ]
    };
    map = new google.maps.Map(document.getElementById("map"),mapProp);
    map.setOptions({styles: styles['hide']});
    const button = document.createElement("button");
    button.textContent = "Planning Journey";
    button.classList.add("MapButton");
    button.addEventListener("click", function () {
        if (!sideBarOpened) {changeSideBar();}
    });
    map.controls[google.maps.ControlPosition.TOP_LEFT].push(button);
    getStations();
    getWeather();
    new AutocompleteDirectionsHandler(map);


}
function getStations() {
    fetch("/stations")
        .then((response) => response.json())
        .then((data) => {
            addMarkers(data);})
}

function addMarkers(stations) {
    // flag for color change 
    let selectedButton = null;
    const button_availablebike = document.createElement("button");
    const button_availablebikestands = document.createElement("button")
    button_availablebike.textContent = "Available Bike";
    button_availablebikestands.textContent = "Available Bikestands";
    button_availablebike.classList.add("btn-design");
    button_availablebikestands.classList.add("btn-design")
    map.controls[google.maps.ControlPosition.TOP_LEFT].push(button_availablebike);
    map.controls[google.maps.ControlPosition.TOP_LEFT].push(button_availablebikestands);

    stations.forEach(station => {

        let markerIcon;
       button_availablebike.addEventListener('click', function(){
        if (selectedButton !== null) {
            selectedButton.style.backgroundColor = '';
            selectedButton.style.color = '';
          }
          this.style.backgroundColor = 'rgb(175, 88, 88)';
          this.style.color = 'white';
          selectedButton = this;
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
    
     button_availablebikestands.addEventListener('click', function(){
       // Update color of selected button
  if (selectedButton !== null) {
    selectedButton.style.backgroundColor = '';
    selectedButton.style.color = '';
  }
  this.style.backgroundColor = 'rgb(175, 88, 88)';
  this.style.color = 'white';
  selectedButton = this;
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
            position: {lat: station.position_lat, lng: station.position_lng},
            map: map,
            icon: markerIcon,
            title: station.name,
            address: station.address,
            station_number: station.number,
             animation: google.maps.Animation.DROP // Add animation property

        });
            //Winnie's codes
        google.maps.event.addListener(map, 'zoom_changed', function() {
            var pixelSizeAtZoom0 = 50; //the size of the icon at zoom level 0
            var maxPixelSize = 50; //restricts the maximum size of the icon, otherwise the browser will choke at higher zoom levels trying to scale an image to millions of pixels

            var zoom = map.getZoom();
            var relativePixelSize = Math.round(pixelSizeAtZoom0*Math.pow(2,zoom)); // use 2 to the power of current zoom to calculate relative pixel size.  Base of exponent is 2 because relative size should double every time you zoom in

            if(relativePixelSize > maxPixelSize) //restrict the maximum size of the icon
                relativePixelSize = maxPixelSize;

            //change the size of the icon
            // marker.setIcon(
            //     new google.maps.MarkerImage(
            //         marker.getIcon().url, //marker's same icon graphic
            //         null,//size
            //         null,//origin
            //         null, //anchor
            //         new google.maps.Size(relativePixelSize, relativePixelSize) //changes the scale
            //     )
            // );
              if (marker.getIcon()) {
                marker.setIcon(
                  new google.maps.MarkerImage(
                    marker.getIcon().url, //marker's same icon graphic
                    null, //size
                    null, //origin
                    null, //anchor
                    new google.maps.Size(relativePixelSize, relativePixelSize) //changes the scale
                  )
                );
              }


        });
        marker.addListener("mouseover", () => {
            marker.setAnimation(google.maps.Animation.BOUNCE);

            const content = `<h1 style="text-align: center; font-size:25px; "> ${station.number} <h1>
            <p style="font-size:20px"> 
            <i class="fa-sharp fa-solid fa-square-parking"></i>
            Available Bikes Stand: ${station.available_bike_stands} 
            </p>
            <p style="font-size:20px">
            <i class="fa-solid fa-person-biking"></i>
            Available Bikes: ${station.available_bikes} 
            </p>
            <p style="font-size:20px">
            <i class="fas fa-check-circle"></i>
            Status: ${station.status}
            </p>`

            infowindow = new google.maps.InfoWindow({content: content});
            infowindow.open({anchor: marker, map: map});
        });
        marker.addListener("mouseout", () => {
            marker.setAnimation(null);
            infowindow.close();
        });
        marker.addListener("click", () => {
            openStationCard(station.number);
        });
    });
}

function openStationCard(number) {
    if (!sideBarOpened) {changeSideBar();}
    let info = document.getElementById("info");
    if (info.innerHTML.trim() !== '') {
        info.innerHTML = '';
    }
    createStationCard(number, "realtime").then(card => {
        info.appendChild(card);
    });
}
async function createStationCard(number, type, data) {

    let card = document.createElement("div");
    card.classList.add("stationCard");
    card.dataset.number = number;
    let station;
    try {
        let response = await fetch("/station/" + number);
        station = await response.json();
    } catch (error) {
        console.error('Error fetching station card data:', error);
    }


    let textDetail = document.createElement("div");
    textDetail.classList.add("textDetail");
    if (type === "predict_orig") {
        textDetail.innerHTML =
            `<h2 >From: ${station.name}</h2>
            <p style="font-size: 25px">Bikes(Predict): ${data}/${station.bike_stands}</p>
            <p style="font-size: 25px">Bonus Support: ${station.bonus == 0 ? 'NO' : 'YES'}</p>
            <p style="font-size: 25px">Banking Support: ${station.banking == 0 ? 'NO' : 'YES'}</p>
            <p style="font-size: 25px">Address: ${station.address}</p>`;
        card.appendChild(textDetail);
        return card;
    }
    if (type === "predict_des") {
        textDetail.innerHTML =
            `<h2 >To: ${station.name}</h2>
            <p style="font-size: 25px">Stands(Predict): ${data}/${station.bike_stands}</p>
            <p style="font-size: 25px">Bonus Support: ${station.bonus == 0 ? 'NO' : 'YES'}</p>
            <p style="font-size: 25px">Banking Support: ${station.banking == 0 ? 'NO' : 'YES'}</p>
            <p style="font-size: 25px">Address: ${station.address}</p>`;
        card.appendChild(textDetail);
        return card;
    }

    textDetail.innerHTML =
        `<h2 >${station.name}</h2>
        <p style="font-size: 25px">Stands: ${station.available_bike_stands}/${station.bike_stands}</p>
        <p style="font-size: 25px">Bikes: ${station.available_bikes}/${station.bike_stands}</p>
        <p style="font-size: 25px">Status: ${station.status}</p>
        <p style="font-size: 25px">Bonus Support: ${station.bonus == 0 ? 'NO' : 'YES'}</p>
        <p style="font-size: 25px">Banking Support: ${station.banking == 0 ? 'NO' : 'YES'}</p>
        <p style="font-size: 25px">Last Update: ${station.last_update}</p>
        <p style="font-size: 25px">Address: ${station.address}</p>`;
    card.appendChild(textDetail);
    let trendButton = document.createElement("button");
    trendButton.classList.add("trendButton");
    // trendButton.setAttribute("id", "trendButton");
    trendButton.textContent = "Show/Hide Trends";
    trendButton.addEventListener("click", function () {trends_switch(trendButton)});
    card.appendChild(trendButton);

    buttonGroup = createButtonGroup();
    let bike_chart = document.createElement("div");
    bike_chart.classList.add("bike_chart");
    let stand_chart = document.createElement("div");
    stand_chart.classList.add("stand_chart");
    card.appendChild(buttonGroup);
    card.appendChild(bike_chart);
    card.appendChild(stand_chart);
    return card;
}
function trends_switch(btn) {
    const card = btn.parentElement;
    const number = card.dataset.number;
    const bike_chart = card.querySelector(".bike_chart");
    const stand_chart = card.querySelector(".stand_chart");
    const buttonGroup = card.querySelector(".button-group");
    if (window.getComputedStyle(bike_chart).getPropertyValue('display') === 'none') {
        bike_chart.style.display = "block";
        stand_chart.style.display = "block"
        buttonGroup.style.display = "flex";
        drawChart(number, "history");
    } else {
        bike_chart.style.display = "none";
        stand_chart.style.display = "none";
        buttonGroup.style.display = "none";
    }
}
function changeSideBar() {
    const leftSection = document.getElementById("leftSection");
    const mapSection = document.getElementById("map");
    // if (leftSection.style.width === "0px" || leftSection.style.width === "") {
    if (!sideBarOpened) {
        leftSection.style.width = "600px";
        mapSection.style.marginLeft = "600px";
        sideBarOpened = true;
    } else {
        leftSection.style.width = "0px";
        mapSection.style.marginLeft = "0px";
        const info = document.getElementById("info");
        info.innerHTML = '';
        sideBarOpened = false;
    }
}


async function drawChart(number, type) {
    let url;
    if (type === "history") {
        url = "/occupancy/" + number;
    } else if (type === "predict_24h") {
        url = "/predict_24h/" + number;
    } else {
        url = "/predict_5d/" + number;
    }
    let response_data;
    try {
        const response = await fetch(url);
        response_data = await response.json();
    } catch (error) {
        console.error('Error fetching occupancy data:', error);
    }
    if (response_data && response_data.length > 0) {
        const bikesData = response_data.map(item => [item.time, item.bikes]);
        const standsData = response_data.map(item => [item.time, item.stands])
        const card = document.querySelector('.stationCard[data-number="' + parseInt(number) + '"]');
        const bike_chart = card.querySelector(".bike_chart");
        const stand_chart = card.querySelector(".stand_chart");
        basicDraw(bikesData, bike_chart);
        basicDraw(standsData, stand_chart);
    } else {
        console.error("Invalid station number!")
    }
}

function basicDraw(bikeData, div) {
    let y;
    if (div.className === "bike_chart") {
        y = "bikes";
    } else {
        y = "stands";
    }
    // Create the data table
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Time');
    data.addColumn('number', y);
    data.addRows(bikeData);

    // Set chart options
    var options = {
        title: 'Occupancy for ' + y + ' at Different Times',
        hAxis: {title: 'Time', titleTextStyle: {color: '#333'}, textPosition: 'none'},
        vAxis: {minValue: 0},
        legend: {position: 'top'},
        height: 300, 
        width: 550, 
        fontSize: 12.5,
        animation: {
            duration: 1000,
            easing: 'out',
            startup: true,
        },
    };

    // Create and draw the chart
    var chart = new google.visualization.LineChart(div);
    chart.draw(data, options);
}
//functions to switch the charts
function selectStatus(clickedButton, status) {
  // Get the parent button group for the clicked button
  const buttonGroup = clickedButton.parentNode;

  // Remove the "selected" class from all buttons in the button group
  const buttons = buttonGroup.getElementsByClassName("chart-button");
  for (let i = 0; i < buttons.length; i++) {
    buttons[i].classList.remove("selected");
  }

  // Add the "selected" class to the clicked button
  clickedButton.classList.add("selected");
  // change charts
    const card = buttonGroup.parentElement;
    const number = card.dataset.number;
    drawChart(number, status);
}
function createButtonGroup() {
    const buttonGroup = document.createElement("div");
    buttonGroup.className = "button-group";

    const buttonNames = ["history", "predict_24h", "predict_5d"];

    for (let i = 0; i < buttonNames.length; i++) {
        const button = document.createElement("button");
        button.className = `chart-button ${buttonNames[i]}`;
        button.textContent = buttonNames[i];
        button.onclick = function () {
            selectStatus(button, buttonNames[i]);
        };
        if (button.textContent === "history") {
            button.classList.add("selected");
        }
        buttonGroup.appendChild(button);
    }

    return buttonGroup;
}

// functions to do recommendation
async function submitForm() {
    event.preventDefault();
  // Collect form data
  const journeyDate = document.getElementById("journeydate").value;
  const journeyTime = document.getElementById("journeytime").value;
  const journeyFrom = document.getElementById("journeyfrom").value;
  const journeyTo = document.getElementById("journeyto").value;
  const journeyMode = document.querySelector('input[name="type"]:checked').value;
  const originLatLng = document.getElementById("origin-lat-lng").value;
  const destinationLatLng = document.getElementById("destination-lat-lng").value;

  // Create FormData object to send data to the backend
  const formData = new FormData();
  formData.append("journeydate", journeyDate);
  formData.append("journeytime", journeyTime);
  formData.append("journeyfrom", journeyFrom);
  formData.append("journeyto", journeyTo);
  formData.append("type", journeyMode);
  formData.append("origin_lat_lng", originLatLng);
  formData.append("destination_lat_lng", destinationLatLng);

  // Send the data to the backend using fetch and handle the response
  try {
    const response = await fetch("/plan", {
      method: "POST",
      body: formData,
    });

    if (response.ok) {
      const data = await response.json();
      // Update the elements on your website based on the response
      //   console.log("test", data);

        let info = document.getElementById("info");
        if (info.innerHTML.trim() !== '') {
         info.innerHTML = '';
        }
        createStationCard(data["orig"]["number"], "predict_orig", data["orig"]["bikes"]).then(card_orig => {
            info.appendChild(card_orig);
        });
        createStationCard(data["des"]["number"], "predict_des", data["des"]["stands"]).then(card_des => {
            info.appendChild(card_des);
        });
    } else {
      console.error("Error in submitting the form");
    }
  } catch (error) {
    console.error("Error in submitting the form", error);
  }

  // Prevent the form from submitting and reloading the page
  return false;
}

