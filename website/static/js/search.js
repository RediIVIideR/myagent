document.addEventListener('DOMSubtreeModified', function() {
    var links = document.getElementsByClassName('page-link');

    for (var i = 0; i < links.length; i++) {
        links[i].addEventListener('click', function(event) {
            page = this.getAttribute('href');
            event.preventDefault(); // Prevent the default behavior of anchor tag
            window.scrollTo({
                top: 0,
                behavior: 'smooth' // For smooth scrolling (if supported)
            });
            check_search(page); // Replace with your actual function
        });
    }
});

function check_search(page) {
    var final_str = '';

    if (page.includes('?page')) {
        var final_str = page;
    } else {
        var final_str = '?';
    }

    var keyword = document.getElementById('search_backend').value;
    final_str = final_str+'&keyword='+keyword;
    var accommodation = document.querySelectorAll('.accommodation');
    var locations = document.querySelectorAll('.location');
    var developers = document.querySelectorAll('.developer');
    var bedding = document.querySelectorAll('.bedding');

    // Convert HTMLCollection to arrays using Array.from()
    accommodation = Array.from(accommodation);
    locations = Array.from(locations);
    developers = Array.from(developers);

    // Loop through checkboxes and push their values to the 'final_str' variable if checked
    accommodation.forEach(checkbox => {
        if (checkbox.checked) {
            final_str = final_str + '&type=' + checkbox.value;
        }
    });

    locations.forEach(checkbox => {
        if (checkbox.checked) {
            final_str = final_str + '&loc=' + checkbox.value;
        }
    });

    developers.forEach(checkbox => {
        if (checkbox.checked) {
            final_str = final_str + '&developer=' + checkbox.value;
        }
    });
    bedding.forEach(checkbox => {
        if (checkbox.checked) {
            final_str = final_str + '&bed=' + checkbox.value;
        }
    });

    fetch('/searching'+final_str, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.text())
    .then(data => {
        document.getElementById('res').innerHTML = data;
 
    });
}

// document.getElementById('search_backend').addEventListener('change', check_search);
document.getElementById('search_backend').oninput = function() {
    var variableToPass = ""; // Replace this with your variable

    // Call the check_search function and pass the variable as an argument
    check_search(variableToPass);
};
document.getElementById('apply').addEventListener('click', function() {
    var variableToPass = ""; // Replace this with your variable

    // Call the check_search function and pass the variable as an argument
    check_search(variableToPass);
});