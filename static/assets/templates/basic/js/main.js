(function($) {
    "use strict";


    // ============== Variables Start ========
    var $testimonails = $('.testimonails');
    // ============== Variables End ========

    // ============== Header Hide Click On Body Js Start ========
    $('.header-button').on('click', function() {
        $('.body-overlay').toggleClass('show')
        if ($('.body-overlay').hasClass('show')) {
            $('.search-box-popup-btn').prop('disabled', true).css('opacity', .5);
        } else {
            $('.search-box-popup-btn').prop('disabled', false).css('opacity', 1);
        }
    });
    $('.body-overlay').on('click', function() {
        $('.header-button').trigger('click')
        $(this).removeClass('show');
    });
    // =============== Header Hide Click On Body Js End =========

    // ==========================================
    //      Start Document Ready function
    // ==========================================
    $(document).ready(function() {

        // ========================== Header Hide Scroll Bar Js Start =====================
        $('.navbar-toggler.header-button').on('click', function() {
            $('body').toggleClass('scroll-hide-sm')
        });
        $('.body-overlay').on('click', function() {
            $('body').removeClass('scroll-hide-sm')
        });
        // ========================== Header Hide Scroll Bar Js End =====================

        // ========================== Category Dropdown Js Start =====================

        $('.category-nav__button').on('click', function() {
            $('.category-nav__button .arrow').toggleClass('rotate');
            $('.dropdown--menu').toggleClass('active');
        });

        $(document).on('click', function(event) {
            var target = $(event.target);

            if (!target.closest('.category-nav__button').length && !target.closest('.dropdown--menu').length) {
                $('.dropdown--menu').removeClass('active');
            }
        });

        // ========================== Category Dropdown Js End =====================

        // ========================== Search Popup Js Start =====================

        $('.search-box-popup-btn').on('click', function() {
            $(this).toggleClass('change-icon');
            $('.navbar .search-box').toggleClass('show');
        });

        $(document).on('click', function(event) {

            if (!$(event.target).closest(".search-box-popup-btn").length) {
                if ($('.navbar .search-box').hasClass('show')) {
                    if (!$(event.target).closest(".search-form").length) {
                        $('.navbar .search-box').removeClass('show');
                        $('.search-box-popup-btn').removeClass('change-icon');
                    }
                }
            }

        });

        // ========================== Search Popup Js End =====================

        // ========================== Add Attribute For Bg Image Js Start =====================
        $(".bg-img").css('background', function() {
            var bg = ('url(' + $(this).data("background-image") + ')');
            return bg;
        });
        // =================================================== Add Attribute For Bg Image Js End =====================

        // ========================== add active class to ul>li to Active current page Js Start =====================
        function dynamicActiveMenuClass(selector) {
            let FileName = window.location.href.split("/").reverse()[0];

            selector.find("li").each(function() {
                let anchor = $(this).find("a");
                if ($(anchor).attr("href") == FileName) {
                    $(this).addClass("active");
                }
            });
            // if any li has active element add class
            selector.children("li").each(function() {
                if ($(this).find(".active").length) {
                    $(this).addClass("active");
                }
            });
            // if no file name return
            if ("" == FileName) {
                selector.find("li").eq(0).addClass("active");
            }
        }
        if ($('ul').length) {
            dynamicActiveMenuClass($('ul'));
        }
        // ========================== add active class to ul>li to Active current page Js End =====================

        // ========================= Slick Slider Js Start ==============
        if ($testimonails.length > 0) {
            var $testimonails_obj = $testimonails.owlCarousel({
                autoplay: false,
                margin: 24,
                loop: true,
                nav: false,
                dots: true,
                items: 3,
                responsiveClass: true,
                responsive: {
                    0: {
                        items: 1,
                        center: false
                    },
                    576: {
                        items: 2,
                        center: false
                    },
                    768: {
                        items: 2,
                    },
                    992: {
                        items: 3,
                    },
                    1200: {
                        items: 3,
                    },
                    1400: {
                        items: 3
                    }
                }
            });
        }
        // ========================= Slick Slider Js End ===================

        // ========================= Odometer Counter Up Js End ==========
        $(".counter-item").each(function() {
            $(this).isInViewport(function(status) {
                if (status === "entered") {
                    for (var i = 0; i < document.querySelectorAll(".odometer").length; i++) {
                        var el = document.querySelectorAll('.odometer')[i];
                        el.innerHTML = el.getAttribute("data-odometer-final");
                    }
                }
            });
        });
        // ========================= Odometer Up Counter Js End =====================

    });
    // ==========================================
    //      End Document Ready function
    // ==========================================

    // ========================= Preloader Js Start =====================
    $(window).on("load", function() {
        $('.preloader').fadeOut();
    })
    // ========================= Preloader Js End=====================

    // ========================= Header Sticky Js Start ==============
    $(window).on('scroll', function() {
        if ($(window).scrollTop() >= 300) {
            $('.header').addClass('fixed-header');
        } else {
            $('.header').removeClass('fixed-header');
        }
    });
    // ========================= Header Sticky Js End===================

    //============================ Scroll To Top Icon Js Start =========
    var btn = $('.scroll-top');

    $(window).scroll(function() {
        if ($(window).scrollTop() > 300) {
            btn.addClass('show');
        } else {
            btn.removeClass('show');
        }
    });

    btn.on('click', function(e) {
        e.preventDefault();
        $('html, body').animate({
            scrollTop: 0
        }, '300');
    });
    //========================= Scroll To Top Icon Js End ======================

    Array.from(document.querySelectorAll('table')).forEach(table => {
        let heading = table.querySelectorAll('thead tr th');
        Array.from(table.querySelectorAll('tbody tr')).forEach((row) => {
            Array.from(row.querySelectorAll('td')).forEach((colum, i) => {
                if (colum.hasAttribute('colspan') && i == 0) {
                    return false;
                }
                colum.setAttribute('data-label', heading[i].innerText)
            });
        });
    });

})(jQuery);