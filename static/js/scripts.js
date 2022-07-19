window.onload = function() {


    // pdisplay operation
    $('#ssearch').submit(function() {
        let sname = $('#sname').val();
        let sstatus = $('#sstatus').val();
        let sgender = $('#sgender').val();
        let sscore =$('#sscore').val();
        

        $.ajax({
            url: '/searchword',
            type: 'POST',
            dataType: 'json',
            data: JSON.stringify({
                'sname': sname,
                'sstatus': sstatus,
                'sgender' : sgender,
                'sscore':sscore
            }),
            contentType:'application/json, charset=UTF-8',
            success: function(data) {
                location.reload();
            },
            error: function(err) {
                console.log(err)
            }
        });
    });
    // to show operation
    $('.updex').click(function() {
        let word_id =$(this).attr('id');
        

        $.ajax({
            url: '/information/' + word_id,
            type: 'POST',
            success: function(data) {
                location.replace("information.html");
            },
            error: function(err) {
                console.log(err)
            }
        });

    });

}

