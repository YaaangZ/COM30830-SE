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
       
      });
      this.directionsRenderer.setMap(map);


    const originInput = document.getElementById("journeyfrom");
    const destinationInput = document.getElementById("journeyto");
    const modeSelector = document.getElementById("mode-selector");
    // Specify just the place data fields that you need.
    const originAutocomplete = new google.maps.places.Autocomplete(
      originInput,
      { fields: ["place_id", "geometry"] }
    );
    // Specify just the place data fields that you need.
    const destinationAutocomplete = new google.maps.places.Autocomplete(
      destinationInput,
      { fields: ["place_id", "geometry"] }

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
  // setupPlaceChangedListener(autocomplete, mode) {
  //   autocomplete.bindTo("bounds", this.map);
  //   autocomplete.addListener("place_changed", () => {
  //     const place = autocomplete.getPlace();
  //
  //     if (!place.place_id) {
  //       window.alert("Please select an option from the dropdown list.");
  //       return;
  //     }
  //
  //     if (mode === "ORIG") {
  //       this.originPlaceId = place.place_id;
  //     } else {
  //       this.destinationPlaceId = place.place_id;
  //     }
  //
  //     this.route();
  //   });
  // }
    setupPlaceChangedListener(autocomplete, mode) {
        autocomplete.bindTo("bounds", this.map);
      autocomplete.addListener("place_changed", () => {
        const place = autocomplete.getPlace();
        // console.log("place:", place);
        if (!place.place_id) {
          window.alert("Please select an option from the dropdown list.");
          return;
        }

        const latLng = `${place.geometry.location.lat()},${place.geometry.location.lng()}`;
        // console.log("latlng:", latLng);
        if (mode === "ORIG") {
          this.originPlaceId = place.place_id;
          document.getElementById("origin-lat-lng").value = latLng;
        } else {
          this.destinationPlaceId = place.place_id;
          document.getElementById("destination-lat-lng").value = latLng;
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