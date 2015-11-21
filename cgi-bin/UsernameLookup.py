#!/usr/bin/python
# Daniel Harris, Gabe Issa, Ethan Lipkind
import cgi
import datetime
import cgitb
cgitb.enable()
import sqlite3
import os
import uuid
import Cookie

form = cgi.FieldStorage()

usr = form['#usr'].value

conn = sqlite3.connect('accounts.db')
c = conn.cursor()

try:
	c.execute('select * from profiles where username=?', (usr,))
	all_results = c.fetchall()

	if len(all_results) < 1:
		print "Content-type: application/json"
		print
		print '{"name": "Profile does not exist."}'
	else:
		print "Content-type: application/json"
		print
		print '{"name": "OK profile exists."}'
except sqlite3.IntegrityError:
	pass