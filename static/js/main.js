(function ($) {
    "use strict";
    
    // Initiate the wowjs
    new WOW().init();


    // Sticky Navbar
    $(window).scroll(function () {
        if ($(this).scrollTop() > 45) {
            $('.nav-bar').addClass('sticky-top');
        } else {
            $('.nav-bar').removeClass('sticky-top');
        }
    });

    // Header carousel
    $(".header-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 1500,
        items: 1,
        dots: true,
        loop: true,
        nav : false,
        // navText : [
        //     '<i class="bi bi-chevron-left"></i>',
        //     '<i class="bi bi-chevron-right"></i>'
        // ]
    });


    // Testimonials carousel
    $(".testimonial-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 1000,
        margin: 24,
        dots: false,
        loop: true,
        nav : true,
        navText : [
            '<i class="bi bi-arrow-left"></i>',
            '<i class="bi bi-arrow-right"></i>'
        ],
        responsive: {
            0:{
                items:1
            },
            992:{
                items:2
            }
        }
    });
    
})(jQuery);

document.addEventListener('DOMContentLoaded', function() {
    if (window.innerWidth < 800) {
        description = document.getElementById('header-text');
        description.innerHTML = '';
        description.classList.remove('p-5');
        description.classList.remove('mt-lg-5');
    }
});