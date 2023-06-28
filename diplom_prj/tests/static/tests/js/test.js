window.onload = initall ;
const url = window.location.href
console.log(url)
var saveAnswerButton
var submitButton
var Question
let radios = document.querySelectorAll('input[type="radio"]')
let checkboxes = document.querySelectorAll('input[type="checkbox"]')
let text = document.querySelector('input[type="text"]')
console.log(radios)

function initall(){
    saveAnswerButton = document.getElementById('save-and-next')
    submitButton = document.getElementById('save-and-submit')
    Question = document.getElementById('prompt').innerHTML
    if (saveAnswerButton != null){
        saveAnswerButton.onclick = saveans
    }
    if (submitButton != null){
        submitButton.onclick = submit
    }
    console.log(Question)
    console.log(saveAnswerButton)
    console.log(submitButton)
    console.log('init закончен')
}


function saveans(){
    var answers = []
    if (radios.length != 0) {   
        for (let radio of radios) {
            if (radio.checked) {
                console.log(radio.value)
            }
        }
    } else if (checkboxes.length != 0) {
        for (let checkbox of checkboxes) {
            if (checkbox.checked) {
                console.log(checkbox.value)
            }
        }
    } else if (text.length != 0) {
        console.log(text.value)
    } else {
        answers.push(null)
    }
    return answers 
}

function submit(){
    
}

$.ajax({
    type: 'GET',
    url: `${url}`,
    dataType: 'json',
    success: function(response){
        console.log(response)
        const data = response.data
    },
    error: function(error){
        console.log(error)
    }
})


