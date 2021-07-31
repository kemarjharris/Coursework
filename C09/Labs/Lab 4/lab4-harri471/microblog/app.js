
const express = require('express');
const app = express();

var bodyParser = require('body-parser');
app.use(bodyParser.json());

let id = 0;
    
let Message = function(author, content){
    this._id = (id++).toString();
    this.author = author;
    this.content = content;
    this.upvote = 0;
    this.downvote = 0;
};

/*  ******* Data types *******
    message objects must have at least the following attributes:
        - (String) messageId 
        - (String) author
        - (String) content
        - (Int) upvote
        - (Int) downvote 

****************************** */ 

let database = [];
    
app.use(function (req, res, next){
    console.log("HTTP request", req.method, req.url, req.body);
    next();
});

app.get("/api/messages/", function (req, res, next) {
    if (req.query.limit) {
        res.json(database.slice(0, req.query.limit));
    } else {
        res.json(database.slice(0, 5));
    }
    
    next();
});

app.get("/api/messages/:id/", function (req, res, next) {
    let index = database.findIndex(function(message){
        return message._id.toString() === req.params.id;
    });
    if (index === -1) {
        res.status(404).send("message id does not exist");
    } else {
        let message = database[index];
        res.json(message);
    }
    next();
});


app.patch("/api/messages/:id/", function (req, res, next) {
    let index = database.findIndex(function(message){
        return message._id.toString() === req.params.id;
    });
    if (index === -1) {
        res.status(404).send("message :" + req.params.id + " does not exists");
    } else {
        let message = database[index];

        if (req.body.action == "downvote") {
            message.downvote+=1;
            res.json(message);
        } else if (req.body.action == "upvote") {
            message.upvote+=1;
            res.json(message);
        } else {
            res.status(404).send("message :" + req.params.id + " does not exists");
        }
    }
    next();
});

app.post('/api/messages/', function (req, res, next) {
    let message = new Message(req.body.author, req.body.content);
    database.unshift(message);
    res.json(message);
    next();
});

app.delete("/api/messages/:id/", function (req, res, next) {
    let index = database.findIndex(function(message){
        return message._id.toString() === req.params.id;
    });
    if (index === -1) {
        res.status(404).send("message :" + req.params.id + " does not exists");
    } else {
        let message = database[index];
        database.splice(index, 1);
        res.json(message);
    }
    next();
});

app.use(express.static('static'));

app.use(function (req, res, next){
    console.log("Storage", JSON.stringify(database, null, 2));
    console.log("HTTP Response", res.statusCode);
});

const http = require('http');
const PORT = 3000;

http.createServer(app).listen(PORT, function (err) {
    if (err) console.log(err);
    else console.log("HTTP server on http://localhost:%s", PORT);
});