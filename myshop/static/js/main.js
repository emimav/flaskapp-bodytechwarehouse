$(window).ready(function() {
    'use strict';
    var bars = $('.menu-toggle'),
        menu = $('.navbar-nav');
    $(bars).click(function(){

        $(this).toggleClass('active');
        $(menu).toggleClass('active');
    });
});