let api = (function(){
    "use strict";
    
    let module = {};

    function send(method, url, data, callback){
        var xhr = new XMLHttpRequest();
        xhr.onload = function() {
            if (xhr.status !== 200) callback("[" + xhr.status + "]" + xhr.responseText, null);
            else callback(null, JSON.parse(xhr.responseText));
        };
        xhr.open(method, url, true);
        if (!data) xhr.send();
        else{
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.send(JSON.stringify(data));
        }
    }
    
    module.addMessage = function(author, content){
        send("POST", "/api/messages/", {author: author, content: content}, function(err, res) {
            if (err) return notifyErrorListeners(err);
            notifyMessageListeners();
        });
        
    };

    module.deleteMessage = function(messageId){
        send("DELETE", "/api/messages/" + messageId + "/", null, function(err, res){
            if (err) return notifyErrorListeners(err);
            notifyMessageListeners();
        });
    };

    let getMessages = function(callback){
        send("GET", "/api/messages/", null, callback);  
    };
    
    module.upvoteMessage = function(messageId){
        send("PATCH", "/api/messages/" + messageId + "/", {action : "upvote"}, function(err, res){
            if (err) return notifyErrorListeners(err);
            notifyMessageListeners();
        });
    };
    
    module.downvoteMessage = function(messageId){
        send("PATCH", "/api/messages/" + messageId + "/",{action : "downvote"} , function(err, res){
            if (err) return notifyErrorListeners(err);
            notifyMessageListeners();
        });
    };
    
    let messageListeners = [];
    
    function notifyMessageListeners(){
        getMessages(function(err, res){
            if (err) return notifyErrorListeners(err);
            messageListeners.forEach(function(listener){
                listener(res);
            });
        });       
    }

    module.onMessageUpdate = function(listener){
        messageListeners.push(listener);
        getMessages(function(err, res) {
            if (err) return notifyErrorListeners(err);
            listener(res);
        });
    };
    
    let voteListeners = [];
    
    function notifyVoteListeners(message){
        voteListeners.forEach(function(listener){
            listener(message);
        });
    }
    
    module.onVoteUpdate = function(listener){
        voteListeners.push(listener);
    };

    let errorListeners = [];

    function notifyErrorListeners(err){
        errorListeners.forEach(function(listener){
            listener(err);
        });
    }

    module.onError = function(listener) {
        errorListeners.push(listener);
    };

    (function refresh(){
        setTimeout(function(e){
            notifyMessageListeners();
            refresh();
        }, 2000);
    }());

    return module;
})();