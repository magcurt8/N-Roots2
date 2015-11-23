

import cgi, Cookie, os, sqlite3
import sys
import BaseHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
# to facilitate debugging
import cgitb
cgitb.enable()

conn = sqlite3.connect('accounts.db')
c = conn.cursor()
HandlerClass = SimpleHTTPRequestHandler
ServerClass  = BaseHTTPServer.HTTPServer
Protocol     = "HTTP/1.0"

if sys.argv[1:]:
    port = int(sys.argv[1])
else:
    port = 8000
server_address = ('127.0.0.1', port)

HandlerClass.protocol_version = Protocol
httpd = ServerClass(server_address, HandlerClass)

sa = httpd.socket.getsockname()
print "Serving HTTP on", sa[0], "port", sa[1], "..."
httpd.serve_forever()

cookie_string = os.environ.get('HTTP_COOKIE')
if cookie_string:
    my_cookie = Cookie.SimpleCookie(cookie_string)
    saved_session_id = my_cookie['session_id'].value

    c.execute('select * from users where sessionID=?', (saved_session_id,))
    all_results = c.fetchall()
    if len(all_results) > 0:
        print "Content-type: text/html"
        print # don't forget newline
        print "<html>"
        print "<body>"
        print "<h1>Welcome back " + all_results[0][0] + "</h1>"
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
    usrname = form['user_name'].value
    password = form['pass_word'].value
    
    # check whether my_name is in accounts.db
    c.execute('select * from users where username=? and password=?;', (usrname,password))
    all_results = c.fetchall()
    if len(all_results) > 0:

        import uuid
        session_id = str(uuid.uuid4())

        c.execute('update users set sessionID=? where username=?',
                  (session_id, usrname))
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
        print "<h1>Hello, " + usrname +". You're now logged in.</h1>"
        print "<h2>session_id: " + session_id + "</h2>"
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

