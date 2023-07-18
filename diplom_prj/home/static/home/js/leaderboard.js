var examSelector
var timeSelector

$(document).ready(function() {
    examSelector = document.getElementById('exam')
    timeSelector = document.getElementById('time')
    resetButton = document.getElementById('reset')
    start_params = createParametrs()
    examSelector.onchange = changeValue
    timeSelector.onchange = changeValue
    resetButton.onclick = resetSelectors
    ajaxRequest(start_params)
})

function ajaxRequest(url) {
    $('#leaderboard-table').empty()
    $('#leaderboard-table').html(`
    <div class="row justify-content-center">
        <div class="col text-center">
            <h3 class="my-3">Loading leaderboard...</h3>
            <div class="d-flex justify-content-center">
                <div class="spinner-border" role="status">
                    <span class="visually-hidden">Loading sign</span>
                </div>
            </div>
        </div>
    </div>
    `) 
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

function resetSelector(options) {
    for (var i = 0, l = options.length; i < l; i++) {
        options[i].selected = options[i].defaultSelected;
    }
}

function resetSelectors() {
    resetSelector(examSelector)
    resetSelector(timeSelector)
    parametrs = start_params
    ajaxRequest(parametrs)
}