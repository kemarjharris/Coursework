const path = require('path');
const express = require('express');
const app = express();

const bodyParser = require('body-parser');
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

app.use(express.static('static'));

var multer  = require('multer');
var upload = multer({ dest: path.join(__dirname, 'uploads')});

var Datastore = require('nedb'),
    messages = new Datastore({ filename: 'db/messages.db', autoload: true, timestampData : true}),
    users = new Datastore({ filename: 'db/users.db', autoload: true });

app.use(function (req, res, next){
    console.log("HTTP request", req.method, req.url, req.body);
    next();
});

var Message = (function(){
    return function item(message){
        this.content = message.content;
        this.username = message.username;
        this.upvote = 0;
        this.downvote = 0;
    };
}());

var User = (function() {
    return function(username, picture) {
        this.username = username;
        this.picture = picture;
    };
}());



// Create

app.post('/api/users/',  upload.single('picture'), function (req, res, next) {
    //if (req.body.username in users) 
    console.log(req.body);
    users.findOne({username: req.body.username}, function(err, doc) {
        if (err) return res.status(500).end(err);
        if (doc != null) return res.status(409).end("Username:" + req.body.username + " already exists");
        else {
            users.insert(new User(req.body.username, req.file), function (err, item) {
            if (err) return res.status(500).end(err);
            // return res.json(item);
            return res.redirect('/');
            });
        }
    });
});

app.post('/api/messages/', function (req, res, next) {
    messages.insert(new Message(req.body), function(err, message) {
        if (err) return res.status(500).end(err);
        else {
            return res.json(message);
        }
    });
});

// Read

app.get('/api/messages/', function (req, res, next) {
    messages.find({}).sort({createdAt:-1}).limit(5).exec(function(err, docs) { 
        if (err) return res.status(500).end(err);
        return res.json(docs);
    });
});

app.get('/api/users/', function (req, res, next) {
    users.find({}).sort({createdAt:-1}).exec(function(err, users) { 
        if (err) return res.status(500).end(err);
        return res.json(users.reverse());
    });
    //return res.json(Object.keys(users));
});

app.get('/api/users/:username/profile/picture/', function (req, res, next) {

    users.findOne({username: req.params.username}, function(err, doc) {
        if (err) return res.status(500).end(err);
        console.log("req.params");
        if (doc == null) res.status(404).end('username ' + req.params.username + ' does not exists');
        else {
            
            console.log(doc);
            let profile = doc.picture;/* retrieve the user's profile from the database */
            res.setHeader('Content-Type', profile.mimetype);
            res.sendFile(profile.path);
        }
    });
});

// Update

app.patch('/api/messages/:id/', function (req, res, next) {
    messages.findOne({_id: req.params.id}, function(err, message) {
        if (err) return res.status(500).end(err);
        if (message == null) return res.status(404).end("Message id:" + req.params.id + " does not exists");
        let upvote = message.upvote;
        let downvote = message.downvote;
        switch (req.body.action){
            case ("upvote"):
                upvote+=1;
                break;
            case ("downvote"):
                downvote+=1;
                break;
        }
        messages.update({_id: req.params.id}, {$set : {upvote: upvote, downvote: downvote}}, function(err) {
            if (err) return res.status(500).end(err);
            return res.json(message);
        });
    });
});

// Delete

app.delete('/api/messages/:id/', function (req, res, next) {
    messages.findOne({ _id: req.params.id}, function(err, doc) {
        if (err) return res.status(500).end(err);
        if (doc == null) return res.status(404).end("Message id:" + req.params.id + " does not exists");

        messages.remove({ _id: req.params.id}, {}, function (err, numRemoved) {
            if (err) return res.status(500).end(err);
            return res.json(doc);
        });
    });
});

const http = require('http');
const PORT = 3000;

http.createServer(app).listen(PORT, function (err) {
    if (err) console.log(err);
    else console.log("HTTP server on http://localhost:%s", PORT);
});