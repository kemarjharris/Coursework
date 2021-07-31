( function () {
    window.addEventListener('load', function(e) {

        let currentImage = api.firstImage();
        let commentPage = 0;
        
        function drawContent(image) {
            let imageElement = document.getElementById("main_image");
            let imageInfo = document.getElementById("image_info");
            imageElement.innerHTML = "";
            imageInfo.innerHTML = "";
            if (image != null) {
                document.getElementById("content_section").style.display = "block";
                // https://www.w3schools.com/howto/howto_css_next_prev.asp
                imageElement.innerHTML = `
                <button class="btn navigation_button" type="button" id = "previous_image">&#8249;</button>
                <div  class = "center">
                <img src="${image.url}" class = "main_image" id = "image_displayed" onError="removeOnError(${image.imageId});">
                <button class="btn" type="button" id = "delete_image">Delete Image</button>
                </div>
                <button class="btn navigation_button" type="button" id = "next_image">&#8250;</button>
                `;
                imageInfo.innerHTML = `
                    <p id ="image_title_text">${image.title}</p>
                    <p>${image.author}</p>
                    <p>${image.date}</p>
                `;
                //https://stackoverflow.com/questions/37232164/how-do-i-delete-an-image-element-if-its-source-file-doesnt-exist?noredirect=1&lq=1
                document.getElementById("image_displayed").onerror = function() {
                    alert("This image link is broken and will be removed from the gallery.");
                    api.deleteImage(image.imageId);
                };
                document.getElementById("next_image").disabled = !api.nextImageExists(image.imageId);
                document.getElementById("previous_image").disabled = !api.prevImageExists(image.imageId);
                imageElement.onclick = function(e) {
                    if (e.target) {
                        if (e.target.id == "delete_image") {
                            api.deleteImage(image.imageId);
                        } else if (e.target.id == "next_image") {
                            currentImage = api.nextImage(image.imageId);
                            commentPage = 0;
                            drawContent(currentImage);
                            
                        } else if (e.target.id == "previous_image") {
                            currentImage = api.previousImage(image.imageId);
                            commentPage = 0;
                            drawContent(currentImage);
                            
                        }
                    }
                };
                comments = api.getComments(image.imageId, commentPage);
                drawComments(comments, image.imageId);
            } else {
                document.getElementById("content_section").style.display = "none";
            }
        }
        
        function drawComments(comments, imageId) {
            document.getElementById("comment_block").innerHTML = "";
            comments.slice().reverse().forEach(function(comment) {
                let elmt = document.createElement('div');
                elmt.className = "comment";
                elmt.innerHTML=`
                    <div class = comment_area>
                        <p class = "comment_author">${comment.author}</p>
                        <button class="btn comment_delete_button" type="button">Delete comment</button>
                    </div>
                    <p class = "comment_content">${comment.content}</p>
                    <p class = "comment_date">${comment.date}</p>
                    <hr>
                `;
                elmt.onclick = function (e) {
                    if (e.target) {
                        if (e.target.className == "btn comment_delete_button") {
                            api.deleteComment(comment.commentId, imageId);
                        }
                    }    
                };
                document.getElementById("comment_block").prepend(elmt);
            });
            document.getElementById("prev_ten").disabled = commentPage <= 0;
            document.getElementById("next_ten").disabled = api.getComments(imageId, commentPage + 1).length <= 0;
        }
        
       

        api.onImageUpdate(function() {
            first = api.firstImage();
            if (currentImage == null || first == null) {
                currentImage = first;
            } else if (api.imageDeleted(currentImage.imageId)) {
                currentImage = api.followingImage(currentImage.imageId);
            }
            drawContent(currentImage);
        });

        api.onCommentUpdate(function(){
            if (currentImage != null) {
                comments = api.getComments(currentImage.imageId, commentPage);
                drawComments(comments, currentImage.imageId);
            }
        });
        

        document.getElementById('image_form').addEventListener('submit', function(e){
            // prevent from refreshing the page on submit
            e.preventDefault();
            // read form elements
            let title = document.getElementById("image_title").value;
            let author = document.getElementById("image_author").value;
            let url = document.getElementById("image_url").value;
            // clean form
            document.getElementById("image_form").reset();
            api.addImage(title, author, url);
        });

        document.getElementById('comment_form').addEventListener('submit', function(e) {
            e.preventDefault();
            let author = document.getElementById("commenter").value;
            let content = document.getElementById("comment_text").value;
           document.getElementById("comment_form").reset();
            api.addComment(currentImage.imageId, author, content);
        });

        document.getElementById("hide_button").addEventListener('click', function(e) {
            e.preventDefault();
            //https://www.geeksforgeeks.org/hide-or-show-elements-in-html-using-display-property/
            document.getElementById("image_form").style.display = "none";
            document.getElementById("show_button").style.display = "block";
        });

        document.getElementById("show_button").addEventListener('click', function(e) {
            e.preventDefault();
            //https://www.geeksforgeeks.org/hide-or-show-elements-in-html-using-display-property/
            document.getElementById("image_form").style.display = "flex";
            document.getElementById("show_button").style.display = "none";
        });

        document.getElementById("comment_navigation").addEventListener('click', function(e) {
            if (e.target) {
                if (e.target.id == "prev_ten") {
                    commentPage--;
                    drawComments(api.getComments(currentImage.imageId, commentPage), currentImage.imageId);
                } else if (e.target.id == "next_ten"){
                    commentPage++;
                    drawComments(api.getComments(currentImage.imageId, commentPage), currentImage.imageId);
                }
            }
        });
    });
})();