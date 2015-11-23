//The server for the project
//front end currently localhost/test.html
//used the code from lectures 11 and 12 to implement the REST API
//implementation of sqlite3 learned and taken from here https://github.com/mapbox/node-sqlite3

var fs = require("fs");
var file = "Database.db";
var exists = fs.existsSync(file);

if(!exists){
	fs.openSync(file, "w");
}

var sqlite3 = require("sqlite3").verbose();
var db = new sqlite3.Database(file);

db.serialize(function() {
	if(!exists){
		db.run("CREATE TABLE peeps (username String NOT NULL PRIMARY KEY, password String NOT NULL, city String NOT NULL, state String NOT NULL, linkedin String Not NULL, googleID String NOT NULL, appleID String NOT NULL");
		db.run("CREATE TABLE companies (name String NOT NULL PRIMARY KEY, type String NOT NULL");
		db.run("CREATE TABLE todolist (username String NOT NULL PRIMARY KEY, type String NOT NULL, input String NOT NULL");
		db.run("CREATE TABLE contactlist (username String NOT NULL PRIMARY KEY, firstname String NOT NULL, lastname String NOT NULL, company String NOT NULL")	
	}  
});

var express = require('express');
var app = express();

//reqired to support parsing of POST request bodies
var bodyParser = require('body-parser');
app.use(bodyParser.json()); //support json encoded bodies
app.use(bodyParser.urlencoded({extended: true})); //support encoded bodies

//put all static files in static_files/ subdirectory
//and the server will serve them from there: e.g.,:
//      http://localhost:3000/test.html
//will send the file static_file/test.html to the user's web browser
app.use(express.static('static_files'));

//Rest API

//post request...create new user
app.post('/users', function(req,res){
	var postBody = req.body;
	var username = postBody.username;
	var password = postBody.password;
	var city = postBody.city;
	var state = postBody.state;
	var country = postBody.country;

	if(!username | !password | !city | !state | !country){
		res.send('ERROR');
		return; //return early
	}

	var stmt = db.prepare("INSERT into peeps VALUES (?,?,?,?,?,?,?)");
	stmt.run(username,password,city,state,linkedin,googleID,appleID);
	stmt.finalize();
	res.send('OK');
	
});

//user get request
app.get('/users/*/*', function(req,res){
	var usernameLookup = req.params[0];
	var pass = req.params[1];
	var sent = 0;
	console.log(usernameLookup);
	console.log(pass);
	db.each('SELECT * FROM peeps', function(err, row){
		console.log(row.username + "   " + row.password);
		if(row.username == usernameLookup & row.password == pass){
			console.log(row);
			res.send(row);
			return;
		}
	});
});

//user delete request
app.delete('/users/*/*', function(req,res){
	var usernameLookup = req.params[0];
	var pass = req.params[1];
	db.delete('DELETE * FROM peeps where username == usernameLookup AND password == pass');
	res.send('OK');
});


// start the server on http://localhost:3000/
var server = app.listen(3000, function () {
  var port = server.address().port;
  console.log('Server started at http://localhost:%s/', port);
});