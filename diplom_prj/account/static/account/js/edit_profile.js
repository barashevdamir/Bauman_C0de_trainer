document.getElementById("profileImage").onclick = function() { document.getElementById("imageUpload").click(); };

function fasterPreview( uploader ) {
    if ( uploader.files && uploader.files[0] ){
        $('#profileImage').attr('src',
            window.URL.createObjectURL(uploader.files[0])
        );
    }
}

document.getElementById("imageUpload").addEventListener("change", function() { fasterPreview( this ); });
$('#imageUpload').on('change', function() {
    var file_data = $('#imageUpload').prop('files')[0];
    var form_data = new FormData();
    form_data.append('file', file_data);

    $.ajax({
        url: '/upload_profile_image/',
        dataType: 'json',
        cache: false,
        contentType: false,
        processData: false,
        data: form_data,
        type: 'post',
        success: function(response) {
            // Успешная загрузка на сервер: обновляем URL изображения
            $('#profileImage').attr('src', response.newImageUrl + '?' + new Date().getTime());
        },
        error: function(response) {
            // Обработка ошибки
            console.log('Error:', response);
        }
    });

});
