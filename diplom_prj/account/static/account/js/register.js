// var signUpButton
//
// $(document).ready(function() {
//     signUpButton = document.getElementById('signUp')
//     signUpButton.onclick = register_user
// })

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$("#register-form").on("submit", function(e) {
    e.preventDefault();
    const csrftoken = getCookie('csrftoken')
    const url = window.location.href  //  начальный урл
    var str = url.slice(0, -9) // обрезаем слеш
    $.ajax({
        url: window.location.href,
        headers: {'X-CSRFToken': csrftoken},
        method: 'POST',
        data: $(this).serialize(),
        dataType: 'json',
        success: function(data) {
            if(data.valid) {
                alert('Registration successful');
                console.log(data)
                window.location.href = `${str}login/`;
                // Perform necessary action after successful validation
            } else {
                $("#error-message").html(data.error);
            }
        }
    });
});

// function register_user() {
//     const csrftoken = getCookie('csrftoken')
//     $.ajax({
//         url: window.location.href,
//         headers: {'X-CSRFToken': csrftoken},
//         method: "POST",
//
//         data: {
//             language: $("#languages").val(),
//             code: editor.getSession().getValue()
//         },
//
//         success: function(response) {
//             document.getElementById("otput").innerHTML = response.output
//         }
//     })
// }