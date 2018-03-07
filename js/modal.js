$(function () {
    $('[data-popup-open]').on('click', function (e) {
        const targeted_popup_class = $(this).attr('data-popup-open');
        document.getElementById(targeted_popup_class).src=`https://www.youtube.com/embed/${targeted_popup_class}?rel=0&autoplay=1`;
        $('[data-popup="' + targeted_popup_class + '"]').appendTo('main');
        $('[data-popup="' + targeted_popup_class + '"]').fadeIn(350);
        e.preventDefault();
    });
    $('[data-popup-close]').on('click', function (e) {
        const targeted_popup_class = $(this).attr('data-popup-close');
        document.getElementById(targeted_popup_class).src='';
        $('[data-popup="' + targeted_popup_class + '"]').fadeOut(350);
        e.preventDefault();
    });
});
