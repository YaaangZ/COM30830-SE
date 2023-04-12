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
    new AutocompleteDirectionsHandler(map);
    getWeather();

}
function getStations() {
    fetch("/stations")
        .then((response) => response.json())
        .then((data) => {
            addMarkers(data);})
}

function addMarkers(stations) {
    stations.forEach(station => {

        let markerIcon;
        if (station.available_bikes >= 25) {
          markerIcon = "../img/greenbike.svg";
        } else if (station.available_bikes >= 10 && station.available_bikes <=24) {
          markerIcon = "../img/bluebike.svg";
        } else if (station.available_bikes <= 9) {
          markerIcon = "../img/redbike.svg";
        }

        let marker = new google.maps.Marker({
            position: {lat: station.position_lat, lng: station.position_lng},
            map: map,
            icon: markerIcon,
            title: station.name,
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
        marker.addListener("mouseover", () => {
            marker.setAnimation(google.maps.Animation.BOUNCE);

            const content = `<div id='infoWindow'>
                <h2 id='infoW_head'>${station.name}</h2>
                <div id='infoW_body'>
                    <p><i class="fa-sharp fa-solid fa-square-parking"></i>
                        Stands: ${station.available_bike_stands}/${station.bike_stands}
                    </p><p><i class="fa-solid fa-person-biking"></i>
                        Bikes: ${station.available_bikes}/${station.bike_stands}
                    </p><p><i class="fas fa-check-circle"></i>
                        Status: ${station.status}
                    </p>
                </div>
            </div>`;

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
    createStationCard(number).then(card => {
        info.appendChild(card);
    });
}
async function createStationCard(number) {
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
    textDetail.innerHTML =
        `<h2>${station.name}</h2>
        <p>Stands: ${station.available_bike_stands}/${station.bike_stands}</p>
        <p>Bikes: ${station.available_bikes}/${station.bike_stands}</p>
        <p>Status: ${station.status}</p>
        <p>Bonus Support: ${station.bonus == 0 ? 'NO' : 'YES'}</p>
        <p>Banking Support: ${station.banking == 0 ? 'NO' : 'YES'}</p>
        <p>Last Update: ${station.last_update}</p>
        <p>Address: ${station.address}</p>`
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
        stand_chart.style.display = "block";
        buttonGroup.style.display = "flex";
        drawChart(number, "history");
    } else {
        bike_chart.style.display = "none";
        stand_chart.style.display = "none"
        buttonGroup.style.display = "none";
    }
}
function changeSideBar() {
    const leftSection = document.getElementById("leftSection");
    const mapSection = document.getElementById("map");
    // if (leftSection.style.width === "0px" || leftSection.style.width === "") {
    if (!sideBarOpened) {
        leftSection.style.width = "400px";
        mapSection.style.marginLeft = "400px";
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


