$(function() {
    $('#btnSignUp').click(function() {

        $.ajax({
            url: '/randomize',
            data: $('form').serialize(),
            type: 'POST',
            error: function(error) {
                console.log(error);
            }
        });
    });
});