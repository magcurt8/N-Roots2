#!/usr/bin/python

import cgi, Cookie, os, sqlite3

# to facilitate debugging
import cgitb
cgitb.enable()

conn = sqlite3.connect('accounts.db')
c = conn.cursor()

cookie_string = os.environ.get('HTTP_COOKIE')
if cookie_string:
    my_cookie = Cookie.SimpleCookie(cookie_string)
    saved_session_id = my_cookie['session_id'].value

    c.execute('select * from peeps where sessionID=?', (saved_session_id,))
    all_results = c.fetchall()
    if len(all_results) > 0:
        print "Content-type: text/html"
        print # don't forget newline
        print "<html>"
        print "<body>"
        print "<h1>Welcome back " + all_results[0][0] + "</h1>"
        #we would need to edit this home page most likely
	    print "<a href = '../home.html'>Go Home</a>"
        print "</body>"
        print "</html>"
    else:
        print "Content-type: text/html"
        print # don't forget newline
        print "<html>"
        print "<body>"
        print "<h1>Error imposter wrong session_id</h1>"
        print "</body>"
        print "</html>"

else:
    form = cgi.FieldStorage()
    user_name = form['username'].value
    pass_word = form['password'].value
    
    # check whether my_name is in accounts.db
    c.execute('select * from peers where username=? and password=?;', (user_name,pass_word))
    all_results = c.fetchall()
    if len(all_results) > 0:

        import uuid
        session_id = str(uuid.uuid4())

        c.execute('update peeps set sessionID=? where username=?',
                  (session_id, user_name))
        conn.commit()

        cook = Cookie.SimpleCookie()
        cook['session_id'] = session_id
 	#cookie expires after one hour
        cook['session_id']['max-age'] = 3600

        print "Content-type: text/html"
        print cook
	    print "Location:        ../home.html"
        print # don't forget newline
        print "<html>"
        print "<body>"
        print "<h1>Hello, " + user_name +". You're now logged in.</h1>"
        print "<h2>session_id: " + session_id + "</h2>"
        #another necessary change in reference here
	    print "<a href = '../home.html'>Go Home</a>"
        print "</body>"
        print "</html>"
    else:
        print "Content-type: text/html"
        print # don't forget newline
        print "<html>"
        print "<body>"
        print "<h1>Sorry unregistered user</h1>"
	    print "<p><a href='../login.html'>Return To Main Page</a></p>"
        print "</body>"
        print "</html>"
