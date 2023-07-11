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
    const loadingMessage = 'Loading';

    let intervalId;
    let pointCount = 0;

    outputElement.html(loadingMessage); // Display initial loading message

    // Start interval to update loading message with varying number of points
    intervalId = setInterval(() => {
        const points = '.'.repeat(pointCount % 4);
        outputElement.html(`${loadingMessage}${points}`);
        pointCount++;
    }, 250);

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
            clearInterval(intervalId); // Stop the loading message interval
            outputElement.empty(); // Clear the loading message
            outputElement.append($(response).find('#output').html());
        },
        error: function() {
            clearInterval(intervalId); // Stop the loading message interval
            outputElement.html('An error occurred.'); // Display error message
        }
    });
}
