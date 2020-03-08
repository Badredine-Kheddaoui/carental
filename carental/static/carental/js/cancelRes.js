$(document).ready(function () {
    function sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    async function demo() {
        let i = 0;
        while (true) {
            $.ajax({
                type: "get",
                url: "/cancellations",
                success: function (msg) {
                    if ($('#cancellation').length === 0 && msg.tag === 'danger') {
                        $('#notification').append('<div id="cancellation" style="margin-bottom: 50px;" class="alert alert-' + msg.tag + '"> ' + msg.message + '</div>');
                    }
                },
                error: function (data) {
                    console.log('An error occurred:');
                    console.log(data);
                },
            });

            await sleep(2000);
            console.log("checking for cancellations..." + ++i);
        }
    }

    demo();

});