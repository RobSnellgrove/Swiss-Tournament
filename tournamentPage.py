#
# DB Forum - a buggy web forum server backed by a good database
#

# The tournamentdb module is where the database interface code goes.
import tournamentdb

# Other modules used to run a web server.
import cgi
import cgitb
cgitb.enable()
from wsgiref.simple_server import make_server
from wsgiref import util

# HTML template for the forum page
HTML_WRAP = '''\
<!DOCTYPE html>
<html>
<head>
<title>Swiss Tournament</title>

<style type = "text/css">
.row-div{
  padding: 10px;
}

th{
  text-align: left;
}

table, th, td{
  border: 1px solid;
  border-collapse:collapse;
  padding: 5px
}

.section-box{
  display:inline-block;
  width: 40%;
  margin: auto;
  font-family: arial;
  border: 1px solid;
  padding: 10px;
  vertical-align: top;
  text-align: top;
}
</style>

</head>

<body>
  <h1>Swiss Tournament</h1>
  <div class = "row-div">
  <div class = "section-box">
    <h2>Register new player</h2>
    <form method=post action="/post">
      <div><input type = "text" id="content" name="newPlayer"></textarea><button id="go" type="submit">Register</button></div>
    </form>
    <form method=post action="/delete">
      <div><select id="playersToDelete" name="playersToDelete"><option selected>-- Choose player to delete --</option>**playersToDelete**</select><button id="delete" type="submit">Delete</button></div>
    </form>
    </div>
  <div class = "section-box">
    <h2>List of registered players</h2>
    <table>
    <tr><th>ID</th><th>Name</th></tr>
    **players**
    </table>
  </div>
</div>
<div class = "row-div">
  <div class = "section-box">
    <h2>Next round</h2>
    <table>
    <tr><th colspan="2">Player 1</th><th colspan="2">Player 2</th><th colspan="2">Winner</th></tr>
    <tr><th>ID</th><th>Name</th><th>ID</th><th>Name</th><th></th><th></th></tr>
    **pairings**
    </table>
  </div>
  <div class = "section-box">
    <h2>Current rankings</h2>
    <table>
    <tr><th>ID</th><th>Name</th><th>Wins</th><th>Losses</th><th>Played</th></tr>
    **standings**
    </table>
  </div>
</div>
</body>
</html>

'''

# HTML template for an individual comment
DROPDOWN = '''/

  <option value="%(id)s">%(id)s | %(name)s</option>

'''

PLAYER = '''\
    <tr><td>%(id)s</td><td>%(name)s</td></tr>
'''

PAIRING = '''\
    <tr><td>%(playerOneId)s</td><td>%(playerOneName)s</td><td>%(playerTwoId)s</td><td>%(playerTwoName)s</td><td><button formaction="tournamentdb.reportMatch(%(playerOneId)s,%(playerTwoId)s)" type="submit">Player1</button></tr>
'''

STANDING = '''\
    <tr><td>%(id)s</td><td>%(name)s</td><td>%(wins)s</td><td>%(losses)s</td><td>%(matches)s</td></tr>
'''

## Request handler for main page
def View(env, resp):
    '''View is the 'main page' of the forum.

    It displays the registration form and the outputs
    '''
    # get posts from database
    players = tournamentdb.GetAllPlayers()
    deletePlayersList = tournamentdb.GetAllPlayers()
    pairings = tournamentdb.getSwissPairings()
    standings = tournamentdb.getStandings()
    # send results
    headers = [('Content-type', 'text/html')]
    resp('200 OK', headers)
    deleteString = ''.join(DROPDOWN % p for p in deletePlayersList)
    playerString = ''.join(PLAYER % p for p in players)
    pairingString = ''.join(PAIRING % q for q in pairings)
    standingString = ''.join(STANDING % p for p in standings)
    newHTML = HTML_WRAP.replace('**playersToDelete**',deleteString).replace('**players**', playerString).replace('**standings**',standingString).replace('**pairings**',pairingString)
    return newHTML
    # The syntax s.join( seq ) where s='-'; and seq = ("a", "b", "c"); would return a-b-c
    # for q in standings is producing a sequence of rows from standings. STANDING % q is subbing each q into the template string STANDING

# Request handler for registering players - inserts to database
def Post(env, resp):
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
        content = fields['newPlayer'][0]
        # If the post is just whitespace, don't save it.
        content = content.strip()
        if content:
            # Save it in the database
            tournamentdb.registerPlayer(content)
    # 302 redirect back to the main page
    headers = [('Location', '/'),
               ('Content-type', 'text/plain')]
    resp('302 REDIRECT', headers) 
    return ['Redirecting']

# Request handler for deleting - inserts to database
def Delete(env, resp):
    # Get post content
    form=cgi.FieldStorage()

    toDeleteID=form['playersToDelete'].value
    tournamentdb.deletePlayer(toDeleteID)
    # 302 redirect back to the main page
    headers = [('Location', '/'),
               ('Content-type', 'text/plain')]
    resp('302 REDIRECT', headers) 
    return ['Redirecting']

## Dispatch table - maps URL prefixes to request handlers
DISPATCH = {'': View,
            'post': Post,
            'delete': Delete,
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

