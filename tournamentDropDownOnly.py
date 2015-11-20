#
# DB Forum - a buggy web forum server backed by a good database
#

# The tournamentdb module is where the database interface code goes.
import tournamentdb

# Other modules used to run a web server.
import cgi
# import cgitb
# cgitb.enable()
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
  <h1>Testing dropdown</h1>
  <div class = "row-div">
  <div class = "section-box">
    <form method=post action="/choose">
      <div>
      <select id="chooseSubject" name="chooseSubject">
          <option selected>-- Choose subject --</option>
          <option value="maths">Maths</option>
          <option value="english">English</option>
          <option value="science">Science</option>
        </select>
        <!--<input type = "text" name = "chooseSubject" autofocus/>-->
      <button id="delete" type="submit">Go</button>
      </div>
    </form>
    </div>
  </div>
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

# Handler for subpage
def Subpage(env, resp):
    '''View is the 'main page' of the forum.

    It displays the registration form and the outputs
    '''
    # send results
    headers = [('Content-type', 'text/html')]
    resp('200 OK', headers)
    return 'subject'

subject = ''

# Request handler for choosing a subject
def Choose(env, resp):
    # Get post content
    input = env['wsgi.input']
    length = int(env.get('CONTENT_LENGTH', 0))
    # If length is zero, post is empty - don't save it.
    if length > 0:
        postdata = input.read(length)
        fields = cgi.parse_qs(postdata)
        content = fields['chooseSubject'][0]
        # If the post is just whitespace, don't save it.
        content = content.strip()
        # if content:
            # Save it in the database
            # tournamentdb.registerPlayer(content)
    # 302 redirect back to the main page
    headers = [('Content-type', 'text/plain')]
    resp('200 OK', headers) 
    return [content]

## Dispatch table - maps URL prefixes to request handlers
DISPATCH = {'': View,
            'choose': Choose,
            'subpage': Subpage,
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

