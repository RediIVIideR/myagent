function uncheck_all() {

    var checkboxes = document.querySelectorAll('input[type="checkbox"]');

            // Find the corresponding checkbox based on the value
            for (var i = 0; i < checkboxes.length; i++) {
                var checkbox = checkboxes[i];
                checkbox.checked = false;
            }
};

document.addEventListener('DOMContentLoaded', function() {
    // Function to parse URL parameters
    function getUrlParameter(name) {
        name = name.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
        var regex = new RegExp('[\\?&]' + name + '=([^&#]*)');
        var results = regex.exec(location.search);
        return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
    };

    // Get URL parameters and check the corresponding checkboxes
    var paramValue = getUrlParameter('loc'); // Change 'param' to your parameter name
    if (location.search.includes('?loc')) {
        var paramValue = getUrlParameter('loc');
        document.querySelector('input[value="'+paramValue+'"]').checked = true;
    } else if (location.search.includes('?type')) {
        var paramValue = getUrlParameter('type');
        document.querySelector('input[value="'+paramValue+'"]').checked = true;
    }
    else if (location.search.includes('?developer')) {
        var paramValue = getUrlParameter('developer');
        document.querySelector('input[value="'+paramValue+'"]').checked = true;
    }
    // Add more conditions for other parameters as needed
});





document.addEventListener('DOMSubtreeModified', function() {
    var links = document.getElementsByClassName('page-link');
    var filter_links_loc = document.getElementsByClassName('one-filter-location');
    var filter_links_dev = document.getElementsByClassName('one-filter-developer');

    for (var i = 0; i < links.length; i++) {
        links[i].addEventListener('click', function(event) {
            page = this.getAttribute('href');
            event.preventDefault();
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
            check_search(page); 
        });
    }

    for (var i = 0; i < filter_links_loc.length; i++) {
        filter_links_loc[i].addEventListener('click', function(event) {
            event.preventDefault(); // Prevent the default behavior of the link
            window.scrollTo({
                top: 0,
                behavior: 'smooth' // For smooth scrolling (if supported)
            });

            // Get the value from the href attribute
            var checkboxValue = this.getAttribute('href')
            uncheck_all();

            // Find the corresponding checkbox based on the value
            var correspondingCheckbox = document.querySelector('input[type="checkbox"][value="' + checkboxValue + '"]');

            // Check the corresponding checkbox
            if (correspondingCheckbox) {
                correspondingCheckbox.checked = true;
            }
            check_search('');
        });
    }
    for (var i = 0; i < filter_links_dev.length; i++) {
        filter_links_dev[i].addEventListener('click', function(event) {
            event.preventDefault(); // Prevent the default behavior of the link
            window.scrollTo({
                top: 0,
                behavior: 'smooth' // For smooth scrolling (if supported)
            });

            // Get the value from the href attribute
            var checkboxValue = this.getAttribute('href');
            uncheck_all();
            var checkboxes = document.querySelectorAll('input[type="checkbox"]');

            // Find the corresponding checkbox based on the value
            for (var i = 0; i < checkboxes.length; i++) {
                var checkbox = checkboxes[i];
            
                // Check if the value contains the target string
                if (checkbox.value.includes(checkboxValue)) {
                    checkbox.checked = true;
                    break; // If you found and checked the checkbox, exit the loop
                }
            }

            check_search('');
        });
    }
})
function check_search(page) {
    var final_str = '';

    if (page.includes('?page')) {
        final_str = page;
    } else if (page.includes('?loc')) {
        final_str = page;
    } else if (page.includes('?developer')) {
        final_str = page;
    } else {
        final_str = '?';
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

document.getElementById('search_backend').oninput = function() {
    var variableToPass = ""; // Replace this with your variable

    // Call the check_search function and pass the variable as an argument
    check_search(variableToPass);
};
document.getElementById('apply').addEventListener('click', function() {
    var variableToPass = ""; // Replace this with your variable

    // Call the check_search function and pass the variable as an argument
    check_search(variableToPass);
})
document.getElementById('clear').addEventListener('click', function() {
    uncheck_all();
    check_search('')
})