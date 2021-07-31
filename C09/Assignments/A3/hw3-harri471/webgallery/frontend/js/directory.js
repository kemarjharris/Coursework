(function() {

    "use strict";
    let page = 0;

    window.onload = function () {
        api.getUser(function (user) {
            if (!user) window.location.replace("/"); 
        });

        document.getElementById("signout_button").addEventListener('click', function() {
            api.signout();
        });

        function drawUsers(users) {
            let userBlock = document.getElementById("users");
            userBlock.innerHTML = "";
            users.forEach(user => {
                let elmt = document.createElement('li');
                elmt.innerHTML=`
                    <a href="gallery/${user._id}" class="gallery_link">${user._id}</a>
                `;
                userBlock.appendChild(elmt);
            });
            document.getElementById("user_prev_ten").disabled = page <= 0;
            api.getUsers(page + 1, function(users) {
                document.getElementById("user_next_ten").disabled = users.length <= 0;
            });
        }
    
        api.onUserUpdate(function() {
            api.getUsers(page, function(users) {
                drawUsers(users);
            });
        });

        //document.getElementById("signout_button").addEventListener('click', api.signout);

        document.getElementById("user_navigation").addEventListener('click', function(e) {
            if (e.target) {
                if (e.target.id == "user_prev_ten") {
                    page--;
                    api.getUsers(page, function(users) {
                        drawUsers(users);
                    });
                    //drawComments(api.getComments(currentImage._id, commentPage), currentImage._id);
                } else if (e.target.id == "user_next_ten"){
                    page++;
                    api.getUsers(page, function(users) {
                        drawUsers(users);
                    });
                }
            }
        });


    };

    

})();