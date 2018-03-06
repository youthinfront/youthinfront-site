(function(){
    function fixTweets() {
        var elements = document.getElementsByTagName("a");
        for(var i = 0; i < elements.length; i++) {
            var element = elements[i];
            var link = element.href;
            if (link.indexOf("twitter.com") != -1) {
                loadTweet(link, element, function(element, data) {
                    console.log(data);
                    element.innerHTML = data.html;
                });
            }
        }
    }

    function loadTweet(link, element, callback) {
        var url = "https://api.twitter.com/1/statuses/oembed.json?url="+link;
        $.ajax({
            url: url,
            dataType: "jsonp",
            success: function(data){
                console.log(data);
                callback(element, data);
            }
        });
    }

    fixTweets();
})();
