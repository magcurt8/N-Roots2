//The server for the project
//front end currently localhost/test.html
//used the code from lectures 11 and 12 to implement the REST API
//implementation of sqlite3 learned and taken from here https://github.com/mapbox/node-sqlite3

var fs = require("fs");
var file = "theDatabase.db";
var exists = fs.existsSync(file);

if(!exists){
	fs.openSync(file, "w");
}

var sqlite3 = require("sqlite3").verbose();
var db = new sqlite3.Database(file);

db.serialize(function() {
	if(!exists){
		db.run("CREATE TABLE peeps (username String NOT NULL PRIMARY KEY, password string NOT NULL, city string NOT NULL, state string NOT NULL, country string NOT NULL)");
		db.run("CREATE TABLE locate (name String NOT NULL PRIMARY KEY, type String NOT NULL, city String NOT NULL, country String NOT NULL");
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

	var stmt = db.prepare("INSERT into peeps VALUES (?,?,?,?,?)");
	stmt.run(username,password,city,state,country);
	stmt.finalize();
	res.send('OK');
	
});

app.get('/users/*/*', function(req,res){
	var usernameLookup = req.params[0];
	var pass = req.params[1];;
	console.log(usernameLookup);
	console.log(pass);
	db.each('SELECT username, password, city, state, country FROM peeps', function(err, row){
		var rowUser = row.username;
		var rowPass = row.password;
		console.log(rowUser + "   " + rowPass);
		if(rowUser == usernameLookup & rowPass == pass){
			res.send(row);
			return;
		}
	});
	res.send({});
});


// start the server on http://localhost:3000/
var server = app.listen(3000, function () {
  var port = server.address().port;
  console.log('Server started at http://localhost:%s/', port);
});