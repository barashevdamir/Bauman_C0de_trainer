const start_page = '?page=1'
var current_page
current_page = start_page
var parametrs
var start_params

var sortSelector
var authSelector
var langSelector
var diffSelector
var tagsSelector
var resetButton

$(document).ready(function() {
    ajaxPagination()
    sortSelector = document.getElementById('sort')
    authSelector = document.getElementById('auth')
    langSelector = document.getElementById('lang')
    diffSelector = document.getElementById('diff')
    tagsSelector = document.getElementById('tags')
    resetButton = document.getElementById('reset')
    start_params = createParametrs()
    parametrs = createParametrs()
    sortSelector.onchange = changeValue
    authSelector.onchange = changeValue
    langSelector.onchange = changeValue
    diffSelector.onchange = changeValue
    tagsSelector.onchange = changeValue
    resetButton.onclick = resetSelectors
})

$(document).ajaxStop(function() {
    ajaxPagination()
})

function ajaxRequest(url, page) {
    $.ajax({
        url: url,
        type: 'GET',
        cache: false,
        dataType: 'html',
        mode: 'same-origin',
        success: (data) => {
            $('#tests-list-view').empty()
            $('#tests-list-view').html(data)
            current_page = page
        }
    })
}

function ajaxPagination() {
    $('#pagination a.bct-btn-page').each((index, el) => {
    $(el).click((e)=> {
        e.preventDefault()
        let page_url = $(el).attr('href')
        let url = page_url + parametrs
        ajaxRequest(url, page_url)
        })
    })
}

function createFilterParametr(e, filter_name) {
    filter_name = '&' + filter_name + '=' + e.value
    return filter_name 
}

function createParametrs() {
    const par1 = createFilterParametr(sortSelector, 'order_by')
    const par2 = createFilterParametr(authSelector, 'login')
    const par3 = createFilterParametr(langSelector, 'language')
    const par4 = createFilterParametr(diffSelector, 'difficulty')
    const par5 = createFilterParametr(tagsSelector, 'tag')
    return par1+par2+par3+par4+par5
}

function changeValue() {
    parametrs = createParametrs()
    let url = start_page + parametrs
    ajaxRequest(url, start_page)
}

function resetSelector(options) {
    for (var i = 0, l = options.length; i < l; i++) {
        options[i].selected = options[i].defaultSelected;
    }
}

function resetSelectors() {
    resetSelector(sortSelector)
    resetSelector(authSelector)
    resetSelector(langSelector)
    resetSelector(diffSelector)
    resetSelector(tagsSelector)
    let url = start_page + start_params
    parametrs = start_params
    ajaxRequest(url, start_page)
}
