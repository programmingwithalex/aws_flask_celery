$(document).ready(function() {
    $('.flash-message .close').on('click', function() {
        $(this).closest('.flash-message').fadeOut();
    });
});