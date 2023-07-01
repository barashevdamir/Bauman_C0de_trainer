const start_page = '?page=1'
var current_page
current_page = start_page
var parametrs

var sortSelector
var langSelector
var diffSelector
var tagsSelector

$(document).ready(function() {
    ajaxPagination()
    sortSelector = document.getElementById('sort')
    langSelector = document.getElementById('lang')
    diffSelector = document.getElementById('diff')
    tagsSelector = document.getElementById('tags')
    const start_params = createParametrs()
    parametrs = start_params
    sortSelector.onchange = changeValue
    langSelector.onchange = changeValue
    diffSelector.onchange = changeValue
    tagsSelector.onchange = changeValue
    console.log(current_page+parametrs)
    console.log('----------')
})

$(document).ajaxStop(function() {
    ajaxPagination()
    console.log(current_page+parametrs)
    console.log('----------')
})

function ajaxPagination() {
    $('#pagination a.bct-btn-page').each((index, el) => {
    $(el).click((e)=> {
        e.preventDefault()
        let page_url = $(el).attr('href')
        let url = page_url + parametrs
        $.ajax({
            url: url,
            type: 'GET',
            success: (data) => {
                $('#tests-list-view').empty()
                $('#pagination').empty()
                $('#tests-list-view').append($(data).find('#tests-list-view').html())
                current_page = page_url
                }
            })
        })
    })
}

function createFilterParametr(e, filter_name) {
    filter_name = '&' + filter_name + '=' + e.value
    return filter_name 
}

function createParametrs() {
    const par1 = createFilterParametr(sortSelector, 'order_by')
    const par2 = createFilterParametr(langSelector, 'language')
    const par3 = createFilterParametr(diffSelector, 'difficulty')
    const par4 = createFilterParametr(tagsSelector, 'tag')
    return par1+par2+par3+par4
}

function changeValue() {
    parametrs = createParametrs()
    let url = start_page + parametrs
    $.ajax({
        url: url,
        type: 'GET',
        success: (data) => {
            $('#tests-list-view').empty()
            $('#pagination').empty()
            $('#tests-list-view').append($(data).find('#tests-list-view').html())
            current_page = start_page
            }
        })
    
}
