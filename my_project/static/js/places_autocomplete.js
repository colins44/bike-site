var initAutocomplete = function(){
    var autocomplete = new google.maps.places.Autocomplete($('input[name="location"]')[0], {types: ['geocode']});

    google.maps.event.addListener(autocomplete, 'place_changed', function() {
        place = autocomplete.getPlace();
        $('input[name="location_id"]').val(place.id);
        $('input[name="latitude"]').val(parseFloat(place.geometry.location.lat().toFixed(4)));
        $('input[name="longitude"]').val(parseFloat(place.geometry.location.lng().toFixed(4)));
        $('input[name="country"]').val(findComponent(place, 'country'));
        $('input[name="post_code"]').val(findComponent(place, 'postal_code'));
        $('input[name="street"]').val(findComponent(place, 'route'));
        $('input[name="street_number"]').val(findComponent(place, "street_number"));
        $('input[name="state"]').val(findComponent(place, 'administrative_area_level_1'));
        $('input[name="city"]').val(findComponent(place, 'administrative_area_level_3') || findComponent(place, 'locality'));
    });
}

function findComponent(result, type) {
  var component = _.find(result.address_components, function(component) {
    return _.include(component.types, type);
  });
  return component && component.short_name;
}
