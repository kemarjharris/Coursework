// eslint-disable-next-line no-unused-vars
let api=(function(){
    "use strict";
    let module = {};

    //localStorage.clear();

    if (!localStorage.getItem("messages")) {
        localStorage.setItem("messages", JSON.stringify({idCount: 0, messageList: []}));
    } 
        
    console.log(localStorage.getItem("messages"));
    
    /*  ******* Data types *******
        message objects must have at least the following attributes:
            - (String) messageId 
            - (String) author
            - (String) content
            - (Int) upvote
            - (Int) downvote 
    
    ****************************** */ 

   //https://www.w3schools.com/js/js_classes.asp
    // add a message
    module.addMessage = function(author, content) {
        let messages = JSON.parse(localStorage.getItem("messages"));
        //https://alligator.io/js/push-pop-shift-unshift-array-methods/
        messages.messageList.unshift({
            author: author,
            content: content,
            upvote: 0,
            downvote: 0,
            messageId: messages.idCount++
        });
        localStorage.setItem("messages", JSON.stringify(messages));
        notifyMessageListeners();
    }
    
    // delete a message given its messageId
    module.deleteMessage = function(messageId){
        let messages = JSON.parse(localStorage.getItem("messages"));
        let index = messages.messageList.findIndex(function(message) {
            return message.messageId == messageId;
        });
        if (index == null) return null;
        messages.messageList.splice(index, 1);
        localStorage.setItem("messages", JSON.stringify(messages));
        notifyMessageListeners();
    }
    
    // return a set of 5 messages using pagination
    // page=0 returns the 5 latest messages
    // page=1 the 5 following ones and so on
    module.getMessages = function(page=0){
        let messages = JSON.parse(localStorage.getItem("messages"));
        let messageList = messages.messageList;
        return messageList.slice(page*5, (page+1)*5);
    }
    
    // upvote a message given its messageId
    module.upvoteMessage = function(messageId){
        let messages = JSON.parse(localStorage.getItem("messages"));
        let index = messages.messageList.findIndex(function(message) {
            return message.messageId == messageId;
        });
        if (index == null) return null;
        messages.messageList[index].upvote ++;
        localStorage.setItem("messages", JSON.stringify(messages));
        notifyVoteListeners();
    }
    
    
    // downvote a message given its messageId
    module.downvoteMessage = function(messageId){
        let messages = JSON.parse(localStorage.getItem("messages"));
        let index = messages.messageList.findIndex(function(message) {
            return message.messageId == messageId;
        });
        if (index == null) return null;
        messages.messageList[index].downvote ++;
        localStorage.setItem("messages", JSON.stringify(messages));
        notifyVoteListeners();
    }

    let messageListeners = [];
    
    function notifyMessageListeners() {
        messageListeners.forEach(function(listener) {
            listener(module.getMessages());
        });
    }

    // register a message listener 
    // to be notified when a message is added or deleted
    module.onMessageUpdate = function(listener){
        messageListeners.push(listener);
        listener(module.getMessages());
    }
    
    let voteListeners = [];

    function notifyVoteListeners() {
        voteListeners.forEach(function(listener) {
            listener(module.getMessages());
        });
    }

    // register a vote listener
    // to be notified when a message is upvoted or downvoted
    module.onVoteUpdate = function(listener){
        voteListeners.push(listener);
        listener(module.getMessages());
    }
    
    return module;
})();