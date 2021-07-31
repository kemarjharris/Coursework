const path = require('path');
const express = require("express");
const app = express();

const fs = require('fs');
const bcrypt = require('bcrypt');
const bodyParser = require("body-parser");
app.use(bodyParser.json());

var multer  = require('multer');
const cookie = require('cookie');
var upload = multer({ dest: path.join(__dirname, 'uploads')});

var Datastore = require('nedb'),
    users = new Datastore({ filename: 'db/users.db', autoload: true }),
    images = new Datastore({ filename: 'db/images.db', autoload: true, timestampData : true}),
    comments = new Datastore({ filename: 'db/comments.db', autoload: true, timestampData : true});

    const session = require('express-session');
    app.use(session({
        secret: 'D06VxWal8gf6AA9LAedc', // random string from https://www.random.org/strings/
        resave: false,
        saveUninitialized: true,
    }));
    
    app.use(function (req, res, next){
        console.log(req.session.username);
        req.username = (req.session.username)? req.session.username : null;
        console.log("HTTP request", req.username, req.method, req.url, req.body);
        next();
    });

var User = (function() {
    return function user(username, hash) {
        this.username = username;
        this.hash = hash;
    };
}());

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

//https://stackoverflow.com/questions/20345936/nodejs-send-html-file-to-client
app.get("/gallery/:profile", function(req, res, next) {
    if (!req.username) return res.redirect("/");
    users.findOne({_id: req.params.profile}, function(err, doc) {
        if (err) return res.status(500).end(err);
        if (doc == null) return res.status(404).end("404: Profile '" + req.params.profile + "' not found");
        res.sendFile('/frontend/gallery.html', {root: __dirname });
    });
});

app.get("/directory", function(req, res, next) {
    if (!req.username) return res.status(401).redirect("/");
    res.sendFile('/frontend/directory.html', {root: __dirname });
});

app.get("/api/loggedIn", function(req, res, next) {
    res.json(req.username);
});

app.get("/api/user/", function(req, res, next) {
    if (!req.username) return res.status(401).end("Access Denied");
    let page = req.query.page ? req.query.page : 0;
    let numUsers = 10;
    users.find({}).sort({createdAt:1}).skip(page * numUsers).limit(numUsers).exec(function(err, docs) {
        if (err) return res.status(500).end(err);
        return res.json(docs);
    });
});

// curl -H "Content-Type: application/json" -X POST -d '{"username":"alice","password":"alice"}' -c cookie.txt localhost:3000/signup/
app.post('/signup/', function (req, res, next) {
    var username = req.body.username;
    var password = req.body.password;
    users.findOne({_id: username}, function(err, user){
        if (err) return res.status(500).end(err);
        if (user) return res.status(409).end("username " + username + " already exists");
        bcrypt.genSalt(function(err, salt) {
            if (err) return res.status(500).end(err);
            bcrypt.hash(password, salt, function(err, hash) {
                if (err) return res.status(500).end(err);
                users.update({_id: username},{_id: username, hash: hash}, {upsert: true}, function(err){
                    if (err) return res.status(500).end(err);
                    req.session.username = req.body.username;
                    // initialize cookie
                    res.setHeader('Set-Cookie', cookie.serialize('username', username, {
                          path : '/', 
                          maxAge: 60 * 60 * 24 * 7
                    }));
                    return res.json("user " + username + " signed up");
                });
            });
        });
    });
});

// curl -H "Content-Type: application/json" -X POST -d '{"username":"alice","password":"alice"}' -c cookie.txt localhost:3000/signin/
app.post('/signin/', function (req, res, next) {
    let username = req.body.username;
    let password = req.body.password;
    // retrieve user from the database
    users.findOne({_id: username}, function(err, user){
        if (err) return res.status(500).end(err);
        if (!user) return res.status(401).end("access denied");
        bcrypt.compare(password, user.hash, function(err, valid) {
            if (err) return res.status(500).end(err);
            if (!valid) return res.status(401).end("access denied");
            req.session.username = req.body.username;
            // initialize cookie
            res.setHeader('Set-Cookie', cookie.serialize('username', username, {
                path : '/', 
                maxAge: 60 * 60 * 24 * 7
            }));
            return res.json("user " + username + " signed in");
        });
    });
});

// curl -b cookie.txt -c cookie.txt localhost:3000/signout/
app.get('/signout/', function (req, res, next) {
    res.setHeader('Set-Cookie', cookie.serialize('username', '', {
          path : '/', 
          maxAge: 60 * 60 * 24 * 7 // 1 week in number of seconds
    }));
    let username = req.username;
    req.session.destroy(function(err) {
        if (err) return res.status(500).end(err);
    });
    return res.json("user " + username + " signed out");
});

app.get('/api/image/:profile/first/', function(req, res, next) {
    if (!req.username) return res.status(401).end("Access Denied");
    images.find({author: req.params.profile}).sort({createdAt:-1}).limit(1).exec(function(err, docs) { 
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
    if (!req.username) return res.status(401).end("Access Denied");
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

app.get("/api/image/:profile/next/:_id", function(req, res, next) {
    if (!req.username) return res.status(401).end("Access Denied");
    images.findOne({ _id: req.params._id}, function(err, doc) {
        if (err) return res.status(500).end(err);
        if (doc == null) return res.status(404).end("Image id: " + req.params._id + " does not exist");
        images.find({date: {$lt : doc.date}, author: req.params.profile}).sort({createdAt:-1}).limit(1).exec(function(err, docs) { 
            if (err) return res.status(500).end(err);
            if (docs.length == 0) {
                return res.status(204).end(); // no image following this one
            }
            return res.json(docs[0]);
        });
    });
});

app.get("/api/image/:profile/previous/:_id", function(req, res, next) {
    if (!req.username) return res.status(401).end("Access Denied");
    images.findOne({ _id: req.params._id}, function(err, doc) {
        if (err) return res.status(500).end(err);
        if (doc == null) return res.status(404).end("Image id:" + req.params._id + " does not exists");
        images.find({date: {$gt : doc.date}, author: req.params.profile}).sort({createdAt:1}).limit(1).exec(function(err, docs) { 
            if (err) return res.status(500).end(err);
            if (docs.length == 0) {
                return res.status(204).send(); // no image following this one
            }
            return res.json(docs[0]);
        });
    });
});

app.get("/api/image/imageDeleted/:_id", function(req, res, next) {
    if (!req.username) return res.status(401).end("Access Denied");
    images.findOne({_id : req.params._id}, function (err, doc) {
        if (err) res.status(500).end(err);
        return res.json(doc == null); // return if the image is found or not, if not assume its deleted
    });
});

app.post("/api/image/", upload.single('picture'), function(req, res, next) {
    if (!(req.body && req.body.title && req.file)) return res.status(400).end("Body missing data");
    if (!(req.username)) return res.status(401).end("Abccess denied");
    users.findOne({_id: req.username}, function (err) {
        if (err) return res.status(500).end(err);
        images.insert(new Image(req.body.title, req.username, new Date(), req.file), function(err, image) {
            if (err) return res.status(500).end(err);
            return res.json(image);
        });
    });
});

app.delete("/api/image/:_id", function(req, res, next) {
    images.findOne({ _id: req.params._id}, function(err, doc) {
        if (err) return res.status(500).end(err);
        if (doc == null) return res.status(404).end("Image id: " + req.params._id + " does not exist");
        if (doc.author != req.username) return res.status(401).end("Access Denied");
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
    if (!req.username) return res.status(401).end("Access Denied");
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
    if (!req.username) return res.status(401).end("Access Denied");
    if (!(req.body && req.body.imageId && req.body.content)) {
        return res.status(400).end("Body missing data");
    }
    images.findOne({ _id: req.body.imageId}, function(err, doc) {
        if (err) return res.status(500).end(err);
        if (doc == null) return res.status(404).end("Image id: " + req.params._id + " does not exist");
        comments.insert(new Comment(req.username, req.body.content, req.body.imageId, new Date()), function(err, comment){
            if (err) return res.status(500).end(err);
            return res.json(comment);
        });
    });
});

app.delete("/api/comment/:commentId", function(req, res, next) {
    comments.findOne({ _id: req.params.commentId}, function(err, comment) {
        if (err) return res.status(500).end(err);
        if (comment == null) return res.status(404).end("Comment id: " + req.params.commentId + " does not exist");
        images.findOne({_id: comment.imageId}, function(err, image) {
            if (err) return res.status(500).end(err);
            if (comment.author !== req.username && image.author !== req.username) return res.status(401).end("access denied");
            comments.remove({ _id: req.params.commentId}, function(err, numRemoved) {
                if (err) return res.status(500).end(err);
                res.json(comment);
            });
        }); 
        
    });
});

app.use(express.static('frontend'));

const http = require('http');
const PORT = 3000;

http.createServer(app).listen(PORT, function (err) {
    if (err) console.log(err);
    else console.log("HTTP server on http://localhost:%s", PORT);
});