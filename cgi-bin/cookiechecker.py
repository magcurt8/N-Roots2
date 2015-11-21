#!/usr/bin/python

# Daniel Harris, Gabe Issa, Ethan Lipkind

import cgi

# to facilitate debugging

import cgitb

cgitb.enable()

import os

cookie_string = os.environ.get('HTTP_COOKIE')
if cookie_string:
    print "Content-type: text/html"
	print "Location:        http://elipkind.rochestercs.org/home.html"
	print # don't forget newline
	print "<html>"
	print "<body>"
	print "</body>"
	print "</html>"