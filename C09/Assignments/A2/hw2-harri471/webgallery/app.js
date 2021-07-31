const path = require('path');
const express = require("express");
const app = express();

const fs = require('fs');

const bodyParser = require("body-parser");
app.use(bodyParser.json());

var multer  = require('multer');
var upload = multer({ dest: path.join(__dirname, 'uploads')});

var Datastore = require('nedb'),
    images = new Datastore({ filename: 'db/images.db', autoload: true, timestampData : true}),
    comments = new Datastore({ filename: 'db/comments.db', autoload: true, timestampData : true});

app.use(function (req, res, next){
    console.log("HTTP request", req.method, req.url, req.body);
    next();
});

var Image = (function(){
    return function image(title, author, date, picture){
        this.title = title;
        this.author = author;
        this.date = date;
        this.picture = picture;
    };
}());

var Comment = (function() {
    return function comment(author, content, imageId, date) {
        this.author = author;
        this.imageId = imageId;
        this.content = content;
        this.date = date;
    };
}());

app.get('/api/image/first/', function(req, res, next) {
    images.find({}).sort({createdAt:-1}).limit(1).exec(function(err, docs) { 
        if (err) return res.status(500).end(err);
        if (docs.length > 0) {
            res.json(docs[0]);
        } else {
            // successful, but no content
            res.status(204).send();
        }
    });
});

app.get("/api/image/:_id", function(req, res, next) {
    images.findOne({_id: req.params._id}, function(err, doc) {
        if (err) return res.status(500).end(err);
        if (doc == null) res.status(404).end('Image id: ' + req.params._id + ' does not exist');
        else {
            let image = doc.picture;/* retrieve the image from the database */
            res.setHeader('Content-Type', image.mimetype);
            res.sendFile(image.path);
        }
    });
});

app.get("/api/image/next/:_id", function(req, res, next) {
    images.findOne({ _id: req.params._id}, function(err, doc) {
        if (err) return res.status(500).end(err);
        if (doc == null) return res.status(404).end("Image id: " + req.params._id + " does not exist");
        images.find({date: {$lt : doc.date}}).sort({createdAt:-1}).limit(1).exec(function(err, docs) { 
            if (err) return res.status(500).end(err);
            if (docs.length == 0) {
                return res.status(204).end(); // no image following this one
            }
            return res.json(docs[0]);
        });
    });
});

app.get("/api/image/previous/:_id", function(req, res, next) {
    images.findOne({ _id: req.params._id}, function(err, doc) {
        if (err) return res.status(500).end(err);
        if (doc == null) return res.status(404).end("Image id:" + req.params._id + " does not exists");
        images.find({date: {$gt : doc.date}}).sort({createdAt:1}).limit(1).exec(function(err, docs) { 
            if (err) return res.status(500).end(err);
            if (docs.length == 0) {
                return res.status(204).send(); // no image following this one
            }
            return res.json(docs[0]);
        });
    });
});

app.get("/api/image/imageDeleted/:_id", function(req, res, next) {
    images.findOne({_id : req.params._id}, function (err, doc) {
        if (err) res.status(500).end(err);
        return res.json(doc == null); // return if the image is found or not, if not assume its deleted
    });
});

app.post("/api/image/", upload.single('picture'), function(req, res, next) {
    if (!(req.body && req.body.title && req.body.author && req.file)) {
        return res.status(400).end("Body missing data");
    }
    images.insert(new Image(req.body.title, req.body.author, new Date(), req.file), function(err, image) {
        if (err) res.status(500).end(err);
        return res.json(image);
    });
});

app.delete("/api/image/:_id", function(req, res, next) {
    images.findOne({ _id: req.params._id}, function(err, doc) {
        if (err) return res.status(500).end(err);
        if (doc == null) return res.status(404).end("Image id: " + req.params._id + " does not exist");
        comments.remove({imageId: req.params._id}, {}, function(err, numRemoved) {
            if (err) return res.status(500).end(err);
        });
        //https://nodejs.org/api/fs.html#fs_file_system
        fs.unlink(doc.picture.path, (err) => {
            if (err) return res.status(500).end(err);
        });
        images.remove({ _id: req.params._id}, {}, function (err, numRemoved) {
            if (err) return res.status(500).end(err);
            return res.json(doc);
        });
    });
});

app.get("/api/comment/:_id/", function(req, res, next) {
    let page = 0; 
    if (req.query.page) {
        page = req.query.page;
    }
    let = numComments = 10;
    images.findOne({ _id: req.params._id}, function(err, image) {
        if (err) return res.status(500).end(err);
        if (image == null) return res.status(404).end("Image id: " + req.params._id + " does not exist");
        // https://docs.mongodb.com/manual/reference/method/cursor.skip/
        comments.find({imageId: req.params._id}).sort({createdAt:1}).skip(page * numComments).limit(numComments).exec(function(err, docs){
            if (err) return res.status(500).end(err);
            return res.json(docs);
        });
    }); 
});

app.post("/api/comment/", function(req, res, next) {
    console.log(req.body);
    if (!(req.body && req.body.imageId && req.body.author && req.body.content)) {
        return res.status(400).end("Body missing data");
    }
    images.findOne({ _id: req.body.imageId}, function(err, doc) {
        if (err) return res.status(500).end(err);
        if (doc == null) return res.status(404).end("Image id: " + req.params._id + " does not exist");
        comments.insert(new Comment(req.body.author, req.body.content, req.body.imageId, new Date()), function(err, comment){
            if (err) return res.status(500).end(err);
            return res.json(comment);
        });
    });
});

app.delete("/api/comment/:commentId", function(req, res, next) {
    comments.findOne({ _id: req.params.commentId}, function(err, doc) {
        if (err) return res.status(500).end(err);
        if (doc == null) return res.status(404).end("Comment id: " + req.params.commentId + " does not exist");
        comments.remove({ _id: req.params.commentId}, function(err, numRemoved) {
            if (err) return res.status(500).end(err);
            res.json(doc);
        });
    });
});

app.use(express.static('static'));

const http = require('http');
const PORT = 3000;

http.createServer(app).listen(PORT, function (err) {
    if (err) console.log(err);
    else console.log("HTTP server on http://localhost:%s", PORT);
});