( function () {
    window.addEventListener('load', function(e) {

        let profile = window.location.pathname;
        profile = decodeURI(profile.substring(profile.lastIndexOf("/") + 1));
        console.log(profile);
        let loggedIn = null;
        let currentImage = null;
        let next = null;
        let prev = null;
        let commentPage = 0;

        api.getUser(function(user) {
            if (!user) return window.location.replace("/");
            loggedIn = user;
            if (loggedIn !== profile) {
                document.getElementById("image_form").style.display = "none";
            } else {
                document.getElementById("image_form").style.display = "flex";
            }
        });

        document.getElementById("signout_button").addEventListener('click', function() {
            api.signout();
        });

        api.onError(function(err){
            console.error("[error]", err);
        });
        
        function drawContent(image) {
            let imageElement = document.getElementById("main_image");
            let imageInfo = document.getElementById("image_info");
            let noImages = document.getElementById("no_Images");
            imageElement.innerHTML = "";
            imageInfo.innerHTML = "";
            noImages.innerHTML = "";
            if (image != null) {
                document.getElementById("content_section").style.display = "block";
                // https://www.w3schools.com/howto/howto_css_next_prev.asp
                if (profile === loggedIn) {
                    imageElement.innerHTML = `
                    <button class="btn navigation_button" type="button" id = "previous_image">&#8249;</button>
                    <div  class = "center">
                    <img src="/api/image/${image._id}" class = "main_image" id = "image_displayed" onError="removeOnError(${image._id});">
                    <button class="btn" type="button" id = "delete_image">Delete Image</button>
                    </div>
                    <button class="btn navigation_button" type="button" id = "next_image">&#8250;</button>
                    `;
                    imageInfo.innerHTML = `
                        <p id ="image_title_text">${image.title}</p>
                        <p>${image.author}</p>
                        <p>${image.date}</p>
                    `;
                } else {
                    imageElement.innerHTML = `
                    <button class="btn navigation_button" type="button" id = "previous_image">&#8249;</button>
                    <div  class = "center">
                    <img src="/api/image/${image._id}" class = "main_image" id = "image_displayed" onError="removeOnError(${image._id});">
                    </div>
                    <button class="btn navigation_button" type="button" id = "next_image">&#8250;</button>
                    `;
                    imageInfo.innerHTML = `
                        <p id ="image_title_text">${image.title}</p>
                        <p>${image.author}</p>
                        <p>${image.date}</p>
                    `;
                }
                
                //https://stackoverflow.com/questions/37232164/how-do-i-delete-an-image-element-if-its-source-file-doesnt-exist?noredirect=1&lq=1
                document.getElementById("image_displayed").onerror = function() {
                    alert("This image link is broken and will be removed from the gallery.");
                    api.deleteImage(image._id);
                };
                document.getElementById("next_image").disabled = next == null;
                document.getElementById("previous_image").disabled = prev == null;

                imageElement.onclick = function(e) {
                    if (e.target) {
                        if (e.target.id == "delete_image") {
                            api.deleteImage(image._id);
                        } else if (e.target.id == "next_image") {
                            api.nextImage(profile, next._id, function(nextImage) {
                                prev = currentImage;
                                currentImage = next;
                                next = nextImage;
                                commentPage = 0;
                                drawContent(currentImage);
                            });
                        } else if (e.target.id == "previous_image") {
                            api.previousImage(profile, prev._id, function(previousImage) {
                                next = currentImage;
                                currentImage = prev;
                                prev = previousImage;
                                commentPage = 0;
                                drawContent(currentImage);
                            });
                        }
                    }
                };
                api.getComments(image._id, commentPage, function(comments) {
                    drawComments(comments, image._id);
                });
            } else {
                document.getElementById("content_section").style.display = "none";
                if (loggedIn !== profile) {
                    noImages.innerHTML = `
                        <p id="no_Images_Text">${profile} has no images in their gallery.</p>
                    `;
                }
            }
        }
        
        function drawComments(comments, _id) {
            document.getElementById("comment_block").innerHTML = "";
            comments.slice().reverse().forEach(function(comment) {
                let elmt = document.createElement('div');
                elmt.className = "comment";
                if (profile === loggedIn || comment.author === loggedIn) {
                    elmt.innerHTML=`
                    <div class = comment_area>
                        <p class = "comment_author">${comment.author}</p>
                        <button class="btn comment_delete_button" type="button">Delete comment</button>
                    </div>
                    <p class = "comment_content">${comment.content}</p>
                    <p class = "comment_date">${comment.date}</p>
                    <hr>
                `;
                } else {
                    elmt.innerHTML=`
                    <div class = comment_area>
                        <p class = "comment_author">${comment.author}</p>
                    </div>
                    <p class = "comment_content">${comment.content}</p>
                    <p class = "comment_date">${comment.date}</p>
                    <hr>
                `;
                }
                
                elmt.onclick = function (e) {
                    if (e.target) {
                        if (e.target.className == "btn comment_delete_button") {
                            api.deleteComment(comment._id);
                        }
                    }    
                };
                document.getElementById("comment_block").prepend(elmt);
            });
            document.getElementById("prev_ten").disabled = commentPage <= 0;
            api.getComments(_id, commentPage + 1, function(comments) {
                document.getElementById("next_ten").disabled = comments.length <= 0;
            });
        }

        api.onImageUpdate(function() {
            if (currentImage == null) {
                api.firstImage(profile, function(first) {
                    currentImage = first;
                    if (currentImage != null) {
                        api.nextImage(profile, currentImage._id, function (nextImage) {
                            next = nextImage;
                            drawContent(currentImage);
                        });
                        
                    } else {
                        drawContent(currentImage);
                    }
                });
            } else {
                // check if image has been deleted 
                api.imageDeleted(currentImage._id, function(deleted) {
                    if (deleted) {
                        if (next != null) {
                            api.nextImage(profile, next._id, function (nextImage) {
                                currentImage = next;
                                next = nextImage;
                                drawContent(currentImage);
                            });
                        } else if (prev != null) {
                            api.previousImage(profile, prev._id, function (previousImage) {
                                currentImage = prev;
                                prev = previousImage;
                                drawContent(currentImage);
                            });
                        } else {
                            currentImage = null;
                            drawContent(currentImage);
                        }
                    } else {
                        api.nextImage(profile, currentImage._id, function (nextImage) {
                            next = nextImage;
                            api.previousImage(profile, currentImage._id, function (previousImage) {
                                prev = previousImage;
                                drawContent(currentImage);
                            });
                        });
                    }
                });
            }    
            
        });

        api.onCommentUpdate(function(){
            if (currentImage != null) {
                api.getComments(currentImage._id, commentPage, function(comments) {
                    if (comments.length <= 0 && commentPage > 0) {
                        commentPage -= 1;
                        api.getComments(currentImage._id, commentPage, function(comments) {
                            drawComments(comments, currentImage._id);
                        });
                    } else {
                        drawComments(comments, currentImage._id);
                    }
                });
            }
        });

        document.getElementById('image_form').addEventListener('submit', function(e){
            // prevent from refreshing the page on submit
            e.preventDefault();
            // read form elements
            let title = document.getElementById("image_title").value;
            let author = document.getElementById("image_author").value;
            let file = document.getElementById("image_file").files[0];
            // clean form
            document.getElementById("image_form").reset();
            api.addImage(title, file);
        });

        document.getElementById('comment_form').addEventListener('submit', function(e) {
            e.preventDefault();
            let content = document.getElementById("comment_text").value;
            document.getElementById("comment_form").reset();
            api.addComment(currentImage._id, content);
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
                    api.getComments(currentImage._id, commentPage, function(comments) {
                        drawComments(comments, currentImage._id);
                    });
                    //drawComments(api.getComments(currentImage._id, commentPage), currentImage._id);
                } else if (e.target.id == "next_ten"){
                    commentPage++;
                    api.getComments(currentImage._id, commentPage, function(comments) {
                        drawComments(comments, currentImage._id);
                    });
                }
            }
        });
    });
})();