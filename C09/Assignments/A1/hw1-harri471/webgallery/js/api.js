let api = (function(){

    if (!localStorage.getItem("images")) {
        localStorage.setItem("images", JSON.stringify({idCount:0, commentIdCount:0, imageList: []}));
    }

    let module = {};

    let imageListeners = [];
    let commentListeners = [];
    
    /*  ******* Data types *******
        image objects must have at least the following attributes:
            - (String) imageId 
            - (String) title
            - (String) author
            - (String) url
            - (Date) date
    
        comment objects must have the following attributes
            - (String) commentId
            - (String) imageId
            - (String) author
            - (String) content
            - (Date) date
    
    ****************************** */ 
    
    // add an image to the gallery
    module.addImage = function(title, author, url){
        let images = loadImages();
        images.imageList.unshift({
            imageId : (images.idCount++).toString(),
            title: title,
            author: author,
            url: url,
            // https://www.w3schools.com/js/js_dates.asp
            date: new Date(),
            commentList: []
        });
        saveImages(images);
        notifyImageListeners();
    };
    
    // delete an image from the gallery given its imageId
    module.deleteImage = function(imageId){
        let images = loadImages();
        let index = imageIndexPreloaded(imageId, images);
        if (index == -1) return null;
        images.imageList.splice(index, 1);
        if (images.imageList.length < 1) {
            curr = -1;
        }
        saveImages(images);
        notifyImageListeners();
    };

    module.imageDeleted = function(imageId) {
        return imageIndex(imageId) < 0;
    };

    module.firstImage = function() {
        let images = loadImages();
        if (images.imageList.length > 0) {
            return images.imageList[0];
        } else {
            return null;
        }
    };

    module.followingImage = function(imageId) {
        let images = loadImages();
        // find the image that was inserted before this one
        let index = images.imageList.findIndex(function(image) {
            return image.imageId < imageId;
        });
        if (index < 0) { // this was the last image, so return whatever was last in the list
            if (images.imageList.length > 0) {
                return images.imageList[images.imageList.length - 1];
            } else {
                return null;
            }
        } else {
            return images.imageList[index];
        }
    };

    module.nextImage = function(imageId) {
        let images = loadImages();
        return images.imageList[imageIndexPreloaded(imageId, images) + 1];
    };

    module.previousImage = function(imageId) {
        let images = loadImages();
        return images.imageList[imageIndexPreloaded(imageId, images) - 1];
    };

    // assumes the image being given always exists
    module.nextImageExists = function(imageId) {
        let imageListLength = loadImages().imageList.length;
        let index = imageIndex(imageId);
        return index + 1 < imageListLength;
    };
    
    module.prevImageExists = function(imageId) {
        let index = imageIndex(imageId);
        return index - 1 >= 0;
    };
    
    // add a comment to an image
    module.addComment = function(imageId, author, content){
        let images = loadImages();
        index = imageIndexPreloaded(imageId, images);
        if (index < 0) return null;
        images.imageList[index].commentList.push({
            commentId : (images.commentIdCount++).toString(),
            imageId: imageId,
            author: author,
            content: content,
            date: new Date()
        });
        saveImages(images);
        notifyCommentListeners();
    };
    
    // delete a comment to an image
    module.deleteComment = function(commentId, imageId){
        let images = loadImages();
        index = imageIndexPreloaded(imageId, images);
        if (index < 0) return null;
        commentIndex = images.imageList[index].commentList.findIndex(function(comment){
            return comment.commentId == commentId;
        });
        if (commentIndex < 0) return null;
        images.imageList[index].commentList.splice(commentIndex, 1);
        saveImages(images);
        notifyCommentListeners();
    };

    module.getComments = function(imageId, page) {
        let images = loadImages();
        let index = imageIndexPreloaded(imageId, images);
        if (index < 0) return [];
        return images.imageList[index].commentList.slice(page * 10, (page + 1) * 10);
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

    function loadImages() {
        return JSON.parse(localStorage.getItem("images"));
    }

    function saveImages(images) {
        localStorage.setItem("images", JSON.stringify(images));
    }

    function imageIndexPreloaded(imageId, images) {
        let index = images.imageList.findIndex(function(image) {
            return image.imageId == imageId;
        });
        return index;
    }

    function imageIndex(imageId) {
        return imageIndexPreloaded(imageId, loadImages());
    }
    
    return module;
})();