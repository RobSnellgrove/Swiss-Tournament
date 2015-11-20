#
# DB Forum - a buggy web forum server backed by a good database
#

# The tournamentdb module is where the database interface code goes.
import tournamentdb

# Other modules used to run a web server.
import cgi
from wsgiref.simple_server import make_server
from wsgiref import util

# HTML template for the forum page
HTML_WRAP = '''\
<!DOCTYPE html>
<html>
<head>
<title>Radio buttons</title>
</head>

<body>
  <h1>Testing dropdown</h1>
  <form method=post action="/selectwinner">
        <input type ="radio" name = "match1" value = "player1">Player 1
        <input type ="radio" name = "match1" value = "player2">Player 2<br>
        <input type ="radio" name = "match2" value = "player3">Player 3
        <input type ="radio" name = "match2" value = "player4">Player 4<br>
      <button id="delete" type="submit">Go</button>
    </form>
</body>
</html>

'''

## Request handler for main page
def View(env, resp):
    '''View is the 'main page' of the forum.

    It displays the registration form and the outputs
    '''
    # send results
    headers = [('Content-type', 'text/html')]
    resp('200 OK', headers)
    return HTML_WRAP
    # The syntax s.join( seq ) where s='-'; and seq = ("a", "b", "c"); would return a-b-c
    # for q in standings is producing a sequence of rows from standings. STANDING % q is subbing each q into the template string STANDING

# Request handler for registering players - inserts to database
def SelectWinner(env, resp):
    '''Post handles a submission of the forum's form.
  
    The message the user posted is saved in the database, then it sends a 302
    Redirect back to the main page so the user can see their new post.
    '''
    # Get post content
    input = env['wsgi.input']
    length = int(env.get('CONTENT_LENGTH', 0))
    # If length is zero, post is empty - don't save it.
    if length > 0:
        postdata = input.read(length)
        fields = cgi.parse_qs(postdata)
        outputString = ''
        if 'match1' in fields:
          match1winner = fields['match1'][0]
          outputString += 'Match 1 winner: ' + match1winner + '<br>'
        if 'match2' in fields:
          match2winner = fields['match2'][0]
          outputString += 'Match 2 winner: ' + match2winner + '<br>'
        # If the post is just whitespace, don't save it.
    # Print out the winners
    headers = [('Content-type', 'text/html')]
    resp('200 OK', headers) 
    return outputString

## Dispatch table - maps URL prefixes to request handlers
DISPATCH = {'': View,
            'selectwinner': SelectWinner,
	    }

## Dispatcher forwards requests according to the DISPATCH table.
def Dispatcher(env, resp):
    '''Send requests to handlers based on the first path component.'''
    page = util.shift_path_info(env)
    if page in DISPATCH:
        return DISPATCH[page](env, resp)
    else:
        status = '404 Not Found'
        headers = [('Content-type', 'text/plain')]
        resp(status, headers)    
        return ['Not Found: ' + page]


# Run this bad server only on localhost!
httpd = make_server('', 8000, Dispatcher)
print "Serving HTTP on port 8000..."
httpd.serve_forever()

