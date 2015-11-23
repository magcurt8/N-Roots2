#!/usr/bin/python
# Daniel Harris, Gabe Issa, Ethan Lipkind
import cgi
import datetime
import cgitb
cgitb.enable()
import sqlite3
import os
import uuid

form = cgi.FieldStorage()
usrname = form['user_name'].value
password = form['pass_word'].value
session_id = str(uuid.uuid4())

conn = sqlite3.connect('accounts.db')
c = conn.cursor()

try:
	adminpassword = form['admin_password'].value
except KeyError:
	adminpassword = 'notadmin'

if adminpassword == 'admin':
	try:
		c.execute('select * from users where username=?;', (usrname,))
		all_results = c.fetchall()

		if len(all_results) > 0:
			
			
			print "Content-type: text/html"

			# don't forget the extra newline!

			print



			print "<html>"

			print "<head><title>CollabRater</title></head>"

			print "<body>"

			print "<h1>Error!</h1>"

			print "<h2>Username already exists. <a href = '../register.html'>Please try another</a></h2>"

			print "<h2>Or <a href='../login.html'>Log In</a></h2>"

			print "</body>"

			print "</html>"

		else:
		
			c.execute('insert into users values(?,?,null,1);', (usrname, password))
			conn.commit()

			print "Content-type: text/html"

			# don't forget the extra newline!

			print



			print "<html>"

			print "<head><title>CollabRater</title></head>"

			print "<body>"

			print "<h1>Account Successfully Created with Admin Privileges</h1>"

			print "<h2><a href='../login.html'>Return to Log In Page</a></h2>"

			print "</body>"

			print "</html>"

	except sqlite3.IntegrityError:
	    pass
else:
	try:
		c.execute('select * from users where username=?;', (usrname,))
		all_results = c.fetchall()

		if len(all_results) > 0:
			
			
			print "Content-type: text/html"

			# don't forget the extra newline!

			print



			print "<html>"

			print "<head><title>CollabRater</title></head>"

			print "<body>"

			print "<h1>Error!</h1>"

			print "<h2>Username already exists. <a href = '../register.html'>Please try another</a></h2>"

			print "<h2>Or <a href='../login.html'>Log In</a></h2>"

			print "</body>"

			print "</html>"

		else:
		
			c.execute('insert into users values(?,?,null,0);', (usrname, password))
			conn.commit()

			print "Content-type: text/html"

			# don't forget the extra newline!

			print



			print "<html>"

			print "<head><title>CollabRater</title></head>"

			print "<body>"

			print "<h1>Account Successfully Created</h1>"

			print "<h2><a href='../login.html'>Return to Log In Page</a></h2>"

			print "</body>"

			print "</html>"

	except sqlite3.IntegrityError:
	    pass

