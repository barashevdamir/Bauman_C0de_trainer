let editor;
let testButton


window.onload = function() {

    editor = ace.edit("editor");
    editor.setTheme("ace/theme/monokai");
    editor.session.setMode("ace/mode/python");

    testButton = document.getElementById("test")
    testButton.onclick = executeCode

}

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



function changeLanguage() {

    let language = $("#languages").val();

    if(language == 'C' || language == 'CPP')editor.session.setMode("ace/mode/c_cpp");
    else if(language == 'PHP')editor.session.setMode("ace/mode/php");
    else if(language == 'PY')editor.session.setMode("ace/mode/python");
    else if(language == 'JS')editor.session.setMode("ace/mode/javascript");
}

function executeCode() {
    const csrftoken = getCookie('csrftoken');
    const outputElement = $('#output');
    outputElement.html('Loading...'); // Display loading message

    $.ajax({
        url: window.location.href,
        headers: {'X-CSRFToken': csrftoken},
        method: "POST",
        async: true, // make the call asynchronous
        data: {
            language: $("#languages").val(),
            code: editor.getSession().getValue()
        },
        success: function(response) {
            outputElement.empty(); // Clear the loading message
            outputElement.append($(response).find('#output').html());
        },
        error: function() {
            outputElement.html('An error occurred.'); // Display error message
        }
    });
}

