// Load the Google Charts library
google.charts.load('current', {'packages':['corechart']});
function initMap() {
    const dublin = {lat: 53.350140, lng: -6.266155};
    const mapProp= {center: dublin, zoom:14};
    map = new google.maps.Map(document.getElementById("map"),mapProp);
    focus = new google.maps.Marker({position: dublin, map: map});
    const button = document.createElement("button");
    button.textContent = "Planning Journey";
    button.classList.add("MapButton");
    button.addEventListener("click", function () {
        if (!sideBarOpened) {
            changeSideBar();
        }
        addNavigation();
    });
    map.controls[google.maps.ControlPosition.TOP_LEFT].push(button);
    getStations();
}
function getStations() {
    fetch("/stations")
        .then((response) => response.json())
        .then((data) => {
            console.log("data is:", typeof data);
            addMarkers(data);})
}

function addMarkers(stations) {
    stations.forEach(station => {
        let marker = new google.maps.Marker({
            position: {lat: station.position_lat, lng: station.position_lng},
            map: map,
            icon: iconImage,
            title: station.name,
            //lable, optimized, animation, drag
        });
        marker.addListener("mouseover", () => {
            marker.setAnimation(google.maps.Animation.BOUNCE);
        });
        marker.addListener("mouseout", () => {
            marker.setAnimation(null);
        });
        marker.addListener("click", () => {
            getAvailability(station.number).then((station_dynamic) => {
                if (infowindow) {infowindow.close();}
                console.log("station_dynamic is:", typeof station_dynamic);
                currentStation = station.number;
                if (sideBarOpened) {stationDetail(currentStation);}
                const content = "<div id='infoWindow'>" +
                    "<h2 id='infoW_head'>" + station.name + "</h2>" +
                    "<div id='infoW_body'>" +
                    "<p>Stands: " + station_dynamic.available_bike_stands + "/" + station.bike_stands + "</p>" +
                    "<p>Bikes: " + station_dynamic.available_bikes + "/" + station.bike_stands + "</p>" +
                    "<p>Status: " + station_dynamic.status + "</p>" +
                    "<p>Address: " + station.address + "</p>" +
                    "<button id='StationDetailButton' onclick='stationDetail(currentStation)'>Show Details</button>" +
                    "</div>" +
                    "</div>";
                infowindow = new google.maps.InfoWindow({content: content});
                infowindow.open({anchor: marker, map: map});

            }).catch((error) => console.error(error));
        });
    });
}
function getAvailability(number) {
    return fetch("/availability/" + number)
    .then((response) => response.json());
}
function stationDetail(number) {
    if (!sideBarOpened) {changeSideBar();}//put into another function
    let info = document.getElementById("info");
    if (info.innerHTML.trim() !== '') {
        info.innerHTML = '';
    }
    stationCard(number).then(card => {
        info.appendChild(card);
        // trends_switch(card.querySelector(".trendButton"));
    });

}
async function stationCard(number) {
    let card = document.createElement("div");
    card.classList.add("stationCard");
    card.dataset.number = number;
    let station;
    let station_dynamic;
    try {
        let response = await fetch("/station/" + number);
        station = await response.json();
        response = await fetch("availability/" + number);
        station_dynamic = await response.json();
    } catch (error) {
        console.error('Error fetching station card data:', error);
    }
    let textDetail = document.createElement("div");
    textDetail.classList.add("textDetail");
    textDetail.innerHTML ="<h2>" + station.name + "</h2>" +
                    "<p>Stands: " + station_dynamic.available_bike_stands + "/" + station.bike_stands + "</p>" +
                    "<p>Bikes: " + station_dynamic.available_bikes + "/" + station.bike_stands + "</p>" +
                    "<p>Status: " + station_dynamic.status + "</p>" +
                    "<p>Address: " + station.address + "</p>";
    card.appendChild(textDetail);
    let trendButton = document.createElement("button");
    trendButton.classList.add("trendButton");
    // trendButton.setAttribute("id", "trendButton");
    trendButton.textContent = "Show/Hide Trends";
    trendButton.addEventListener("click", function () {trends_switch(trendButton)});
    card.appendChild(trendButton);
    let bike_chart = document.createElement("div");
    bike_chart.classList.add("bike_chart");
    let stand_chart = document.createElement("div");
    stand_chart.classList.add("stand_chart");
    card.appendChild(bike_chart);
    card.appendChild(stand_chart);
    return card;
}
function trends_switch(btn) {
    const card = btn.parentElement;
    const number = card.dataset.number;
    const bike_chart = card.querySelector(".bike_chart");
    const stand_chart = card.querySelector(".stand_chart");
    if (window.getComputedStyle(bike_chart).getPropertyValue('display') === 'none') {
        bike_chart.style.display = "block";
        stand_chart.style.display = "block"
        drawChart(number);
    } else {
        bike_chart.style.display = "none";
        stand_chart.style.display = "none"
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
function addNavigation() {
    document.getElementById("Navigation").style.display = "block";
}
// Function to draw the chart
async function drawChart(number) {
    let response_data;
    try {
        const response = await fetch("/occupancy/" + number);
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
        hAxis: {title: 'Time', titleTextStyle: {color: '#333'}},
        vAxis: {minValue: 0},
        legend: {position: 'top'},
        animation: {
            duration: 1000,
            easing: 'out',
            startup: true,
        },
    };

    // Create and draw the chart
    var chart = new google.visualization.ColumnChart(div);
    chart.draw(data, options);
}
let map = null;
// src: https://www.flaticon.com/free-icons/bike?word=bike
const iconImage = "../img/bikeIcon.png";//24px
let infowindow;
let focus;
let currentStation;
let sideBarOpened = false;
// window.initMap = initMap;
// initMap()
//continue: 1 icon resize and color
// 2. add event to show info and popup
//click

