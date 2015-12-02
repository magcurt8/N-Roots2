#!/usr/bin/python

# Remember to make this executable: chmod a+x week8-lab.py
import sqlite3
import cgi

# to facilitate debugging
import cgitb
cgitb.enable()

form = cgi.FieldStorage()
stuff = form['stuff'].value

conn = sqlite3.connect('accounts.db')
c = conn.cursor()

try:
	c.execute('select * from peeps where username=?', (stuff,))
	all_results = c.fetchall()
	if len(all_results) > 0:
		print "Content-type: application/json"
		print
		print '{"name": "Not Valid"}'
	else:
		print "Content-type: application/json"
		print
		print '{"name": "Valid"}'
except sqlite3.IntegrityError:
	pass