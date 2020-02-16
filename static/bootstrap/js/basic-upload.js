$(function () {


    $(".js-upload-photos").click(function () {
        var title = $('#id_title').val();
        var description = $('#id_description').val();

        if (title == '' || description == '') {
            alert('Lütfen title ve description bilgisi giriniz!!');
        } else {
            $("#id_title").prop("disabled", true);
            $("#id_description").prop("disabled", true);

            $.ajax({
                url: 'basic-upload-first',
                data: {
                    'title': title,
                    'description': description,

                },
                success: function (data) {
                    console.log(data);
                }
            })
        }


        $("#fileupload").click();
    });


    $("#fileupload").fileupload({
        dataType: 'json',
        sequentialUploads: true,
        start: function (e) {
            $("#modal-progress").modal("show");
        },
        stop: function (e) {
            $("#modal-progress").modal("hide");
        },
        progressall: function (e, data) {
            var progress = parseInt(data.loaded / data.total * 100, 10);
            var strProgress = progress + "%";
            $(".progress-bar").css({"width": strProgress});
            $(".progress-bar").text(strProgress);
        },
        done: function (e, data) {
            if (data.result.is_valid) {
                $("#gallery tbody").prepend(

                )
            }
        }
    });

});