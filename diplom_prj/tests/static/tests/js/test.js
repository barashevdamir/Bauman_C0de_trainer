window.onload = initall

var saveAnswerButton
var submitButton
var goBackButton
var questionId
var test_answers = JSON.parse(localStorage.getItem('test_answers'))

let radios = document.querySelectorAll('input[type="radio"]')
let checkboxes = document.querySelectorAll('input[type="checkbox"]')
let text = document.querySelector('input[type="text"]')

function initall(){
    saveAnswerButton = document.getElementById('save-and-next')
    submitButton = document.getElementById('save-and-submit')
    goBackButton = document.getElementById('confidently-go-back')
    questionId = document.getElementsByClassName('prompt')[0].id
    if (saveAnswerButton != null){
        saveAnswerButton.onclick = saveans
    }
    if (submitButton != null){
        submitButton.onclick = submit
    }
    goBackButton.onclick = clearStorage
    console.log({'data': 'answers'})
    console.log(JSON.parse(localStorage.getItem('test_answers')))
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

function grabValues(inputs, checkedValues) {   
    for (let input of inputs) {
        if (input.checked) {
            checkedValues.push(input.value)
        }
    }
    if (checkedValues.length == 0) {
        checkedValues.push(null)
    }
}

function saveans(){
    var answers = []
    if (radios.length != 0) {   
        grabValues(radios, answers)
    } else if (checkboxes.length != 0) {
        grabValues(checkboxes, answers)
    } else if (text != null && text.value != "") {
        answers.push(text.value)
    } else {
        answers.push(null)
    }
    if (test_answers != null) {
        test_answers[ questionId ] = answers
        localStorage.setItem('test_answers', JSON.stringify(test_answers))
    } else {
        localStorage.setItem('test_answers', JSON.stringify({[questionId]: answers}))  
    }
}

function submit(){
    saveans()
    const csrftoken = getCookie('csrftoken')
    const url = window.location.href
    $.ajax({
        type: 'POST',
        url: `${url.slice(0, url.lastIndexOf('/') + 1)}save/`,
        headers: {'X-CSRFToken': csrftoken},
        mode: 'same-origin',
        dataType: 'json',
        data: {answers: localStorage.getItem('test_answers')}, // отвратительно передает данные
        success: function(response){
            console.log(response)
        },
        error: function(error){
            console.log(error)
        }
    })
    localStorage.removeItem('test_answers')
}

function clearStorage() {
    localStorage.removeItem('test_answers')
}