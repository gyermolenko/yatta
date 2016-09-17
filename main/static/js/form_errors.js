$("#id_username").change(function () {
    var uname = $(this);
    var form = uname.closest("form");
    var error_msg = $("<span />").addClass("ajax-error");

    $(".ajax-error", $(form)).remove();

    $.ajax({
        url: form.attr("data-validate-username-url"),
        data: form.serialize(),
        dataType: 'json',
        success: function (data) {
            if (data.is_taken) {
                error_msg.text(data.error_message).insertAfter(uname);
            }
        }
    });

});
