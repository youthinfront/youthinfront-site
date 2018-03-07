(function(){
    function fixTweets() {
        var elements = document.getElementsByTagName("a");
        for(var i = 0; i < elements.length; i++) {
            var element = elements[i];
            var link = element.href;
            if (link.indexOf("twitter.com") != -1) {
                embedTweet(link, element, function(element, data) {
                    element.innerHTML = data.html;
                });
            } else if ((link.indexOf("youtube.com") != -1) || (link.indexOf("youtu.be/") != -1)) {
                embedYoutube(link, element, function(element, data) {
                    console.log(data);
                });
            }
        }
    }

    function embedTweet(link, element, callback) {
        var url = "https://api.twitter.com/1/statuses/oembed.json?url="+link;
        $.ajax({
            url: url,
            dataType: "jsonp",
            success: function(data){
                callback(element, data);
            }
        });
    }

    function embedYoutube(link, element, callback) { 
        var id = extractYoutubeVideoId(link);

        //https://www.youtube.com/watch?v=FdeioVndUhs
        //https://youtu.be/FdeioVndUhs

        var url = "https://api.twitter.com/1/statuses/oembed.json?url="+link;
        var width = window.innerWidth
        var height = width*.5625

        var url = "https://www.youtube.com/embed/" + id + "?rel=0";
        //element.innerHTML = '<iframe width="' + width + '" height="' + height + '"' + 'src="' + url + '" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>'
        //element.innerHTML = '<iframe width="560 height="290" ' + 'src="' + url + '" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>'
        element.innerHTML = '<iframe width="560" height="315" src="' + url + '" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>'
    }

    function extractYoutubeVideoId(link) {
        var id = null;
        if (link.indexOf("youtube.com") != -1) { 
            var tag1 = "?v=";
            var tag2 = "&v=";
            var tag = tag1;;
            var startOfTag = link.indexOf(tag1);
            if (startOfTag == -1) {
                startOfTag = link.indexOf(tag2);
                tag = tag2;
            }        
            var id = removeBeforeInclusive(link, tag);
            id = removeAfter(id, "&");
            id = removeAfter(id, "/");
            return id;
        } else if (link.indexOf("youtu.be/") != -1) {   
            var tag = "youtu.be/";
            var id = removeBeforeInclusive(link, tag);
            id = removeAfter(id, "&");
            id = removeAfter(id, "/");
            return id;
        }
        return null
    }

    function removeAfter(string, terminator) {
        if (string.indexOf(terminator) != -1) {
            string = string.substring(0, string.indexOf(terminator));
        }
        return string;
    }

    function removeBeforeInclusive(string, tag) {
        var startOfTag = string.indexOf(tag);
        var endOfTag = startOfTag + tag.length;
        var id = string.substring(endOfTag, string.length);
        return id;
    }

    fixTweets();
})();
