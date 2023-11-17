function uncheck_all() {

    var checkboxes = document.querySelectorAll('input[type="checkbox"]');

            // Find the corresponding checkbox based on the value
            for (var i = 0; i < checkboxes.length; i++) {
                var checkbox = checkboxes[i];
                checkbox.checked = false;
            }
};

function uncheck(classname) {

    var checkboxes = document.querySelectorAll('.'+classname);

            // Find the corresponding checkbox based on the value
            for (var i = 0; i < checkboxes.length; i++) {
                var checkbox = checkboxes[i];
                checkbox.checked = false;
            }
};

function query(array, type, btn_class){
    final_str = '';
    any_checked = false;
    array.forEach(element => {
        if (element.checked) {
            final_str = final_str + type + element.value;
            any_checked = true
        }
    });
    if (any_checked) {
        // Add an additional class to the button
        document.querySelector('button.'+btn_class).classList.add('btn-filters-active');
    }
    else{
        document.querySelector('button.'+btn_class).classList.remove('btn-filters-active');
    }
    return final_str

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
    var status = document.querySelectorAll('.status');
    var accommodation = document.querySelectorAll('.accommodation');
    var locations = document.querySelectorAll('.location');
    var developers = document.querySelectorAll('.developer');
    var bedding = document.querySelectorAll('.bedding');

    // Convert HTMLCollection to arrays using Array.from()
    status = Array.from(status);
    accommodation = Array.from(accommodation);
    locations = Array.from(locations);
    developers = Array.from(developers);
    bedding = Array.from(bedding);

    // Loop through checkboxes and push their values to the 'final_str' variable if checked

    final_str = final_str + query(accommodation,'&type=','accommodation');
    final_str = final_str + query(locations,'&loc=','location');
    final_str = final_str + query(developers,'&developer=','developer');
    final_str = final_str + query(bedding,'&bed=','bedding');
    final_str = final_str + query(status,'&status=','status');

    minprice = document.getElementById('range-min').value;
    maxprice = document.getElementById('range-max').value;
    priceButton = document.getElementsByClassName('price')[0];

    if (minprice !== '200000' || maxprice !== '30000000') {
        priceButton.classList.add('btn-filters-active');
    } else {
        priceButton.classList.remove('btn-filters-active');
    }


    final_str = final_str+'&minprice='+minprice+'&maxprice='+maxprice;
    console.log(final_str);

    fetch('/searching'+final_str, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.text())
    .then(data => {
        console.log(data);
        document.getElementById('res').innerHTML = data;
 
    });
}

document.getElementById('search_backend').oninput = function() {
    var variableToPass = ""; // Replace this with your variable
    check_search(variableToPass);
};

document.addEventListener('DOMContentLoaded', function() {
    var clearButtons = document.getElementsByClassName('clear');
    var applyButtons = document.getElementsByClassName('apply');
    console.log(applyButtons);

    var applyButtonsArray = Array.from(applyButtons);
    var clearButtonsArray = Array.from(clearButtons);
    applyButtonsArray.forEach(function(applyButton) {
        applyButton.addEventListener('click', function() {
            check_search("");
        });
    });
    clearButtonsArray.forEach(function(clearButton) {
        clearButton.addEventListener('click', function() {
            uncheck(clearButton.id);
            check_search('');
        });
    });

    if (window.innerWidth > 1200) {
        document.getElementById('filter_menu').classList.add('justify-content-center');
        document.getElementsByClassName('indicate-scroll')[0].style = 'font-size:0px';
        document.getElementsByClassName('indicate-scroll')[1].style = 'font-size:0px';
    }
    else{
        document.getElementById('filter_menu').classList.remove('justify-content-center')
    };




    let input_loc = document.getElementById("search_loc");
    let list_loc = document.querySelectorAll(".search_loc_item");

    let input_dev = document.getElementById("search_dev");
    let list_dev = document.querySelectorAll(".search_dev_item");

    function search (input, list){
    for(let i = 0; i < list.length; i += 1){
    if(list[i].innerText.toLowerCase().includes(input.value.toLowerCase())){
        list[i].style.display = "block";
    }else{
        list[i].style.display = "none";
    }
    }
    }

    input_dev.addEventListener('input', function(event) {
        search(this, list_dev); 
    });

    input_loc.addEventListener('input', function(event) {
        search(this, list_loc); 
    });

    document.getElementById('clear-price').addEventListener('click',function () {
        document.getElementById('price-filter').innerHTML = `<div class="price-input">
        <div class="field">
          <span>Min AED</span>
          <input type="number" class="input-min" value="200000">
        </div>
        <div class="separator">-</div>
        <div class="field">
          <span>Max AED</span>
          <input type="number" class="input-max" value="30000000">
        </div>
      </div>
      <div class="slider">
        <div class="progress"></div>
      </div>
      <div class="range-input">
        <input type="range" class="range-min" id="range-min" min="200000" max="30000000" value="200000" step="100000">
        <input type="range" class="range-max" id="range-max" min="0" max="30000000" value="30000000" step="500000">
      </div>`;

      check_search('')
        
    });

    document.getElementById('clear-all').onclick = function(){
        uncheck_all();
        document.getElementById('clear-price').click();
        check_search('');
    }
});



