function initMap() {
  // Create a map object and specify the DOM element for display.
  var map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: -34.397, lng: 150.644},
    scrollwheel: false,
    zoom: 8
  });
}

var initAutocomplete = function(){
    var autocomplete = new google.maps.places.Autocomplete($('input[name="location"]')[1], {types: ['geocode']});

    google.maps.event.addListener(autocomplete, 'place_changed', function() {
        var place = autocomplete.getPlace();
        $('input[name="location_id"]').val(place.id);
        $('input[name="location_lat"]').val(place.geometry.location.lat());
        $('input[name="location_lng"]').val(place.geometry.location.lng());
        $('input[name="location_country"]').val(findComponent(place, 'country'));
        $('input[name="location_state"]').val(findComponent(place, 'administrative_area_level_1'));
        $('input[name="location_city"]').val(findComponent(place, 'administrative_area_level_3') || findComponent(place, 'locality'));
    });
}

function findComponent(result, type) {
  var component = _.find(result.address_components, function(component) {
    return _.include(component.types, type);
  });
  return component && component.short_name;
}
