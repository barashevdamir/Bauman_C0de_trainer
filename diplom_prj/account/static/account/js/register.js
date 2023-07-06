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



function validateUsername(username) {
    if (!validateUsernameFormat(username)) {
        alert('Invalid username format. Only alphanumeric characters and underscores are allowed.');
        return;
    }

    $.ajax({
        url: 'validate_username/',
        data: {
            'username': username,
            'csrfmiddlewaretoken': '{{ csrf_token }}'
        },
        dataType: 'json',
        success: function(data) {
            if (data.is_taken) {
                alert('This username is already taken.');
            }
        },
        error: function(jqXHR, textStatus, errorThrown) {
            console.error('Error:', textStatus, errorThrown);
            alert('Something went wrong. Please try again later.');
        }
    });
}
function validateUsernameFormat(username) {
    var re = /^[a-zA-Z0-9_]+$/;
    return re.test(String(username));
}
function validateEmail(email) {
    if (!validateEmailFormat(email)) {
        alert('Please enter a valid email.');
        return;
    }

    $.ajax({
        url: 'validate_email/',
        data: {
            'email': email,
            'csrfmiddlewaretoken': '{{ csrf_token }}'
        },
        dataType: 'json',
        success: function(data) {
            if (data.is_taken) {
                alert('This email is already in use.');
            }
        },
        error: function(jqXHR, textStatus, errorThrown) {
            console.error('Error:', textStatus, errorThrown);
            alert('Something went wrong. Please try again later.');
        }
    });
}

function validateEmailFormat(email) {
    var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(email).toLowerCase());
}
