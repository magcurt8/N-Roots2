#!/usr/bin/python

import cgi
import datetime
import cgitb
cgitb.enable()
import sqlite3
import os
import uuid

form = cgi.FieldStorage()
user_name = form['username'].value
pass_word = form['password'].value
ci_ty = form['city'].value
sta_te = form['state'].value
google_id = form['googleid'].value
apple_id = form['appleid'].value
session_id = str(uuid.uuid4())

#Creation of database
conn = sqlite3.connect('accounts.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS peeps (username String NOT NULL PRIMARY KEY, password String NOT NULL, city String NOT NULL, state String NOT NULL, linkedin String Not NULL, googleID String NOT NULL, appleID String NOT NULL, sessionID)''')
c.execute('''CREATE TABLE IF NOT EXISTS companies (name String NOT NULL PRIMARY KEY, type String NOT NULL)''')
c.execute('''CREATE TABLE IF NOT EXISTS todolist (username String NOT NULL PRIMARY KEY, type String NOT NULL, input String NOT NULL)''')
c.execute('''CREATE TABLE IF NOT EXISTS contactlist (username String NOT NULL PRIMARY KEY, firstname String NOT NULL, lastname String NOT NULL, company String NOT NULL)''')

try:
	c.execute('select * from users where username=?;', (user_name,))
	all_results = c.fetchall()

	if len(all_results) > 0:
		
		
		print "Content-type: text/html"

		# don't forget the extra newline!

		print



		print "<html>"

		print "<head><title>N-Roots</title></head>"

		print "<body>"

		print "<h1>Error!</h1>"

		print "<h2>Username already exists. <a href = '../register.html'>Please try another</a></h2>"

		print "<h2>Or <a href='../login.html'>Log In</a></h2>"

		print "</body>"

		print "</html>"

	else:
	
		c.execute('insert into users peeps(?,?,?,?,?,?,?,null);', (user_name, pass_word, ci_ty, sta_te, google_id, apple_id))
		conn.commit()

		print "Content-type: text/html"

		# don't forget the extra newline!

		print



		print "<html>"

		print "<head><title>N-Roots</title></head>"

		print "<body>"

		print "<h1>Account Successfully Created</h1>"

		print "<h2><a href='../login.html'>Return to Log In Page</a></h2>"

		print "</body>"

		print "</html>"

except sqlite3.IntegrityError:
    pass