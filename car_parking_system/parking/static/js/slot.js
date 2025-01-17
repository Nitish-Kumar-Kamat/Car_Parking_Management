function fetchParks() {
    var level = document.getElementById('level').value;
    var parkDropdown = document.getElementById('parking_number');
    parkDropdown.innerHTML = '';  // Clear previous options

    fetch(`/get_available_parks/?level=${level}`)
        .then(response => response.json())
        .then(data => {
            data.parks.forEach(function(parking_number) {
                var option = document.createElement('option');
                option.text = parking_number;
                option.value = parking_number;
                parkDropdown.add(option);
            });
        })
        .catch(error => console.error('Error:', error));
}
