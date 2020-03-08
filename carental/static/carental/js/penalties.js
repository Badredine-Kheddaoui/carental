$(document).ready(function () {
    function sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    async function demo() {
        let i = 0;
        while (true) {
            $.ajax({
                type: "get",
                url: "/penalties",
                success: function (msg) {
                    if ($('#penalty').length === 0 && msg.tag === 'danger') {
                        $('#notification').append('<div id="penalty" style="margin-bottom: 50px;" class="alert alert-' + msg.tag + '"> ' + msg.message + '</div>');
                    }
                },
                error: function (data) {
                    console.log('An error occurred:');
                    console.log(data);
                },
            });

            await sleep(2000);
            console.log("checking for penalties..." + ++i);
        }
    }

    demo();

});