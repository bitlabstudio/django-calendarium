$(document).ready(function() {
    $('#result_list input[type="text"]').each(function() {
        $('<div class="preview" style="background-color: #' + $(this).val() + ';">').insertBefore($(this));
    });
});