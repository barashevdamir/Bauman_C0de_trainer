window.onload = initall

var goBackButton
var test_answers = JSON.parse(localStorage.getItem('test_result'))

function initall() {
    goBackButton = document.getElementById('back-to-tests')
    document.getElementById("TestTitle").innerHTML = test_answers.test
    document.getElementById("passed").innerHTML = test_answers.passed
    document.getElementById("score").innerHTML = test_answers.score
    document.getElementById("exp").innerHTML = test_answers.exp_gain
    document.getElementById("correct").innerHTML = test_answers.correct
    document.getElementById("incorrect").innerHTML = test_answers.incorrect
    document.getElementById("unanswered").innerHTML = test_answers.unanswered
    goBackButton.onclick = clearStorage
}

function clearStorage() {
    localStorage.removeItem('test_result')
}