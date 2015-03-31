// the URL of the WAMP Router (Crossbar.io)
//
var wsuri;
if (document.location.origin == "file://") {
    wsuri = "ws://127.0.0.1:8080/ws";

} else {
    wsuri = (document.location.protocol === "http:" ? "ws:" : "wss:") + "//" +
    document.location.host + "/ws";
}

// the WAMP connection to the Router
//
var connection = new autobahn.Connection({
    url: wsuri,
    realm: "realm1"
});

connection.onopen = function (session) {
    main(session);
};
function main(session) {
    session.call("getdf").then(function (df) {
        $("#df").val(df[0] + " / " + df[1]);
    });
    session.call("getfree").then(function (free) {
        $("#free").val(free[0] + " / " + free[1]);
    });
    session.subscribe("getdf", function (df) {
        $("#df").val(df[0][0] + " / " + df[0][1]);
    });
    session.subscribe("getfree", function (free) {
        $("#free").val(free[0][0] + " / " + free[0][1]);
    });
    //获取视频信息
    $("#search-enter").click(function () {
        $("#search-results").html("");
        session.call("getfileinfo", [$("#search-field").val()]).then(
            function (result) {
                html = tmpl('tpllist', JSON.parse(result));
                $("#search-results").html(html);
                calld(session, result)
            },
            function (faild) {
                $("#search-results").html("<br> <p>获取视频信息失败，请重试</p>");
            }
        )
    })
}

function calld(session, result) {
    var items = document.getElementById("result-items").getElementsByTagName("li");
    for (var i = 0; i < items.length; i++) {
        items[i].onclick = function (evt) {
            var height = (evt.target.innerText.trim().match(/^\d{3}/) || [""])[0];
            var ext = evt.target.innerText.trim().match(/\w{3,4}$/)[0];
            $("#result-items").html("");
            session.call("calldownload", [JSON.parse(result).url, ext, height]).then(
                function (uuid) {
                    $("#progressbar").css("display","block");
                    $("#additioninfo").css("display","block");
                    session.subscribe(uuid, function (progress) {
                        $(".pro-bar").css("width",progress[0][0]+"%");
                        $("#filesiza").html("文件大小: "+ progress[0][1]);
                        $("#speed").html("当前速度: " + progress[0][2]);
                        $("#eta").html("预估时间: "+ progress[0][3]);
                    });
                }
            );
        }
    }
}


// now actually open the connection
//
connection.open();


;
(function () {
    var cache = {};

    this.tmpl = function tmpl(str, data) {
        // Figure out if we're getting a template, or if we need to
        // load the template - and be sure to cache the result.
        var fn = !/\W/.test(str) ?
            cache[str] = cache[str] ||
            tmpl(document.getElementById(str).innerHTML) :

            // Generate a reusable function that will serve as a template
            // generator (and which will be cached).
            new Function("obj",
                "var p=[],print=function(){p.push.apply(p,arguments);};" +

                    // Introduce the data as local variables using with(){}
                "with(obj){p.push('" +

                    // Convert the template into pure JavaScript
                str
                    .replace(/[\r\t\n]/g, " ")
                    .split("<%").join("\t")
                    .replace(/((^|%>)[^\t]*)'/g, "$1\r")
                    .replace(/\t=(.*?)%>/g, "',$1,'")
                    .split("\t").join("');")
                    .split("%>").join("p.push('")
                    .split("\r").join("\\'")
                + "');}return p.join('');");

        // Provide some basic currying to the user
        return data ? fn(data) : fn;
    };
})();