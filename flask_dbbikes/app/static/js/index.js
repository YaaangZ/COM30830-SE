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
                currentStation = {station: station, station_dynamic: station_dynamic};
                if (sideBarOpened) {stationDetail(currentStation);}
                const content = "<div id='infoWindow'>" +
                    "<h2 id='infoW_head'>" + station.name + "</h2>" +
                    "<div id='infoW_body'>" +
                    "<p>Stands: " + station_dynamic.available_bike_stands + "/" + station.bike_stands + "</p>" +
                    "<p>Bikes: " + station_dynamic.available_bikes + "/" + station.bike_stands + "</p>" +
                    "<p>Status: " + station_dynamic.status + "</p>" +
                    "<p>Address: " + station.address + "</p>" +
                    "<button id='StationDetailButton' onclick='stationDetail(currentStation)'>Show Trends</button>" +
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
function stationDetail(detail) {
    let stationDetail = document.getElementById("stationDetail");
    if (stationDetail) {stationDetail.remove();}
    if (!sideBarOpened) {changeSideBar();}
    let info = document.createElement("div");
    info.setAttribute("id", "stationDetail");
    let station = detail.station;
    let station_dynamic = detail.station_dynamic;
    info.innerHTML ="<h2>" + station.name + "</h2>" +
                    "<p>Stands: " + station_dynamic.available_bike_stands + "/" + station.bike_stands + "</p>" +
                    "<p>Bikes: " + station_dynamic.available_bikes + "/" + station.bike_stands + "</p>" +
                    "<p>Status: " + station_dynamic.status + "</p>" +
                    "<p>Address: " + station.address + "</p>";
    document.getElementById("leftSection").appendChild(info);
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
        sideBarOpened = false;
    }
}
function addNavigation() {
    document.getElementById("Navigation").style.display = "block";
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

