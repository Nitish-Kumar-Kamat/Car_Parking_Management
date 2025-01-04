function fetchSlots() {
    var level = document.getElementById('level').value;
    var slotDropdown = document.getElementById('slot');
    slotDropdown.innerHTML = '';  // Clear previous options

    fetch(`/get_available_slots/?level=${level}`)
        .then(response => response.json())
        .then(data => {
            data.slots.forEach(function(slot) {
                var option = document.createElement('option');
                option.text = slot;
                option.value = slot;
                slotDropdown.add(option);
            });
        })
        .catch(error => console.error('Error:', error));
}
