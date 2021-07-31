var api = (function(){

    "use strict";
    
    var module = {};

    function sendFiles(method, url, data, callback){
        let formdata = new FormData();
        Object.keys(data).forEach(function(key){
            let value = data[key];
            formdata.append(key, value);
        });
        let xhr = new XMLHttpRequest();
        xhr.onload = function() {
            if (xhr.status == 204) callback(null, null); // No content
            else if (xhr.status !== 200) callback("[" + xhr.status + "]" + xhr.responseText, null);
            else callback(null, JSON.parse(xhr.responseText));
        };
        xhr.open(method, url, true);
        xhr.send(formdata);
    }

    function send(method, url, data, callback){
        var xhr = new XMLHttpRequest();
        xhr.onload = function() {
            if (xhr.status == 204) callback(null, null); // No content
            else if (xhr.status !== 200) callback("[" + xhr.status + "]" + xhr.responseText, null);
            else callback(null, JSON.parse(xhr.responseText));
        };
        xhr.open(method, url, true);
        if (!data) xhr.send();
        else{
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.send(JSON.stringify(data));
        }
    }

   let imageListeners = [];
   let commentListeners = [];


   module.getUser = function(callback) {
     send("GET", "/api/loggedIn", null, function(err, res) {
        if (err) notifyErrorListeners(err);
        callback(res);
     });
   };

   module.getUsers = function(page, callback) {
       send("GET", "/api/user?page=" + page.toString(), null, function (err, res) {
            if (err) notifyErrorListeners(err);
            callback(res);
       });
   };

    module.firstImage = function(profile, callback) {
        send("GET", "/api/image/"+profile+"/first/", null, function(err, res) {
            if (err) notifyErrorListeners(err);
            callback(res);
        });
    };

    module.nextImage = function(profile, _id, callback) {
        send("GET", "/api/image/"+profile+"/next/" + _id + "/", null, function(err, res) {
            if (err) return notifyErrorListeners(err);
            callback(res);
        });
    };
    
    module.previousImage = function(profile, _id, callback) {
        send("GET", "/api/image/"+profile+"/previous/" + _id + "/", null, function(err, res) {
            if (err) return notifyErrorListeners(err);
            callback(res);
        });
    };

    module.imageDeleted = function(_id, callback) {
        send("GET", "/api/image/imageDeleted/" + _id + "/", null, function(err, res) {
            if (err) return notifyErrorListeners(err);
            callback(res);
        });
    };

    module.addImage = function(title, file){
        sendFiles("POST", "/api/image/", {title: title, picture: file}, function(err, res) {
            if (err) return notifyErrorListeners(err);
            notifyImageListeners();
        });
        
    };

    // delete an image from the gallery given its _id
    module.deleteImage = function(_id){
        send("DELETE", "/api/image/" + _id + "/", null, function(err, res) {
            if (err) return notifyErrorListeners(err);
            notifyImageListeners();
        });
        
    };
    
    module.getComments = function(_id, page, callback) {
        send("GET", "/api/comment/" + _id + "?page=" + page.toString(), null, function(err, res) {
            if (err) return notifyErrorListeners(err);
            callback(res);
        });
    };
    
    // add a comment to an image
    module.addComment = function(imageId, content){
        send("POST", "/api/comment/", {imageId: imageId, content: content}, function(err, res) {
            if (err) return notifyErrorListeners(err);
            notifyCommentListeners();
        });
    };
    
    // delete a comment to an image
    module.deleteComment = function(commentId){
        send("DELETE", "/api/comment/" + commentId + "/", null, function(err, res) {
            if (err) return notifyErrorListeners(err);
            notifyCommentListeners();
        });
        
    };
    
    // call handler when an image is added or deleted from the gallery
    module.onImageUpdate = function(handler){
        imageListeners.push(handler);
        handler();
    };

    // call handler when a comment is added or deleted to an image
    module.onCommentUpdate = function(handler){
        commentListeners.push(handler);
        handler();
    };

    function notifyImageListeners() {
        imageListeners.forEach(function(listener) {
            listener(); // do all for whatever this is
        });
    }

    function notifyCommentListeners() {
        commentListeners.forEach(function(listener) {
            listener(); // do all for whatever this is
        });
    }

    let errorListeners = [];

    function notifyErrorListeners(err){
        errorListeners.forEach(function(listener){
            listener(err);
        });
    }

    module.onError = function(listener) {
        errorListeners.push(listener);
    };

    
    let userListeners = [];
    
    let getUsername = function(){
        return document.cookie.replace(/(?:(?:^|.*;\s*)username\s*\=\s*([^;]*).*$)|^.*$/, "$1");
    };
    
    function notifyUserListeners(){
        userListeners.forEach(function(listener){
            listener();
        });
    }
    
    module.onUserUpdate = function(listener){
        userListeners.push(listener);
        listener();
    };
    
    module.signin = function(username, password){
        send("POST", "/signin/", {username, password}, function(err, res){
             if (err) return notifyErrorListeners(err);
             notifyUserListeners();
        });
    };
    
    module.signup = function(username, password){
        send("POST", "/signup/", {username, password}, function(err, res){
             if (err) return notifyErrorListeners(err);
             notifyUserListeners(getUsername());
        });
    };

    module.signout = function(){
        send("GET", "/signout/", null, function(err){
            if (err) return notifyErrorListeners(err);
            window.location.replace("/");
       });
    };

	/*
    (function refresh(){
        setTimeout(function(e){
            notifyImageListeners();
            refresh();
        }, 2000);
    }());
    
    */

    return module;
})();
