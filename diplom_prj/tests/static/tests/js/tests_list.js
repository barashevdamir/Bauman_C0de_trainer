function ajaxPagination() {
    $('#pagination a.bct-btn-page').each((index, el) => {
    $(el).click((e)=> {
        e.preventDefault()
        console.log(e)
        console.log(el)
        let page_url = $(el).attr('href')
        console.log(page_url)
        $.ajax({
            url: page_url,
            type: 'GET',
            success: (data) => {
                $('#tests-list-view').empty()
                $('#pagination').empty()
                $('#tests-list-view').append($(data).find('#tests-list-view').html())
                }
            })
        })
    })
}

$(document).ready(function() {
    ajaxPagination()
})

$(document).ajaxStop(function() {
    ajaxPagination()
})