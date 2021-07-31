/* eslint-disable no-undef */
( function() {
    "use strict"

    function redraw(messages) {
        // clear out items
        document.getElementById("messages").innerHTML = '';
        //https://stackoverflow.com/questions/32682962/javascript-angular-loop-through-array-backwards-with-foreach
        messages.slice().reverse().forEach(function(message) {
            // draw each message
            // create a new message element
            let elmt = document.createElement('div');
            elmt.className = "message";
            elmt.innerHTML=`
                <div class="message_user">
                    <img class="message_picture" src="media/user.png" alt="${message.author}">
                    <div class="message_username">${message.author}</div>
                </div>
                <div class="message_content">${message.content}</div>
                <div class="upvote-icon icon">${message.upvote}</div>
                <div class="downvote-icon icon">${message.downvote}</div>
                <div class="delete-icon icon"></div>
            `;

            elmt.addEventListener('click', function(e) {
                if (e.target) {
                    if (e.target.className == "upvote-icon icon"){
                        api.upvoteMessage(message.messageId);
                    } else if (e.target.className == "downvote-icon icon") {
                        api.downvoteMessage(message.messageId);
                    }   else if (e.target.className == "delete-icon icon") {
                        api.deleteMessage(message.messageId);
                    }
                }    
            });

            document.getElementById("messages").prepend(elmt);
        });
    }

    window.addEventListener('load', function () {

        api.onMessageUpdate(function(messages) {
            redraw(messages);
        });

        api.onVoteUpdate(function(messages) {
            redraw(messages);   
        });
    
        document.getElementById('create_message_form').addEventListener('submit', function(e){
            // prevent from refreshing the page on submit
            e.preventDefault();
            // read form elements
            let username = document.getElementById("post_name").value;
            let content = document.getElementById("post_content").value;
            // clean form
            document.getElementById("create_message_form").reset();
            api.addMessage(username, content);
        });
    });
    
}());
