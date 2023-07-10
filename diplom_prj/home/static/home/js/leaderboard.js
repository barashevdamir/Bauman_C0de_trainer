var examSelector
var timeSelector

$(document).ready(function() {
    examSelector = document.getElementById('exam')
    timeSelector = document.getElementById('time')
    // resetButton = document.getElementById('reset')
    start_params = createParametrs()
    examSelector.onchange = changeValue
    timeSelector.onchange = changeValue
    // resetButton.onclick = resetSelectors
    ajaxRequest(start_params)
})

function ajaxRequest(url) {
    $.ajax({
        url: url,
        type: 'GET',
        cache: false,
        dataType: 'html',
        mode: 'same-origin',
        success: (data) => {
            $('#leaderboard-table').empty()
            $('#leaderboard-table').html(data)
            }
        })
}

function createFilterParametr(e, filter_name, symbol) {
    filter_name = symbol + filter_name + '=' + e.value
    return filter_name 
}

function createParametrs() {
    const par1 = createFilterParametr(examSelector, 'exam', '?')
    const par2 = createFilterParametr(timeSelector, 'time', '&')
    return par1+par2
}

function changeValue() {
    let parametrs = createParametrs()
    ajaxRequest(parametrs)
}