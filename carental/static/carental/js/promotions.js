$(document).ready(function () {
    function sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    async function demo() {
        let i = 0;
        while (true) {
            $.ajax({
                type: "get",
                url: "/promotion",
                success: function (msg) {
                    if ($('#promotion').length === 0) {
                        $('#notification').append('<div id="promotion" style="margin-bottom: 50px;" class="alert alert-' + msg.tag + '"> ' +
                            'A new promotion on <span style="font-size: 20px; color: red">' + msg.car +
                            ' (-' + msg.percentage + '%)</span> valid untill ' + msg.end + '</div>');
                    }

                },
                error: function (data) {
                    console.log('An error occurred:');
                    console.log(data);
                },
            });

            await sleep(2000);
            console.log("checking for promotions..." + ++i);
        }
    }

    demo();

});