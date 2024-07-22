$(document).on('click', '#add-cart', function (e) {
    e.preventDefault();
    $.ajax({
        type: 'POST',
        uri: '{% url 'cart_add' %}',

    })
})