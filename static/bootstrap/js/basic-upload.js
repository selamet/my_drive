$(function () {

    $('#yuklendi').hide();

    $(".js-upload-photos").click(function () {
        $("#fileupload").click();
    });


    $("#fileupload").fileupload({
        dataType: 'json',
        sequentialUploads: true,
        start: function (e) {
            $("#modal-progress").modal("show");
            $("#kapat").hide();
        },
        stop: function (e) {
            $("#modal-progress").modal("hide");
            alert('Dosyalar başarı ile yüklendi Ana sayfaya yönlendiriliyorsunuz');
            location.href = "/"
        },
        progressall: function (e, data) {
            var progress = parseInt(data.loaded / data.total * 100, 10);
            var strProgress = progress + "%";
            $(".progress-bar").css({"width": strProgress});
            $(".progress-bar").text(strProgress);
        },
        done: function (e, data) {

        }
    });

});