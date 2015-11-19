#
# Database access functions for the web forum.
# 

import time
import psycopg2



## Get posts from database.
def GetAllPlayers():
    '''Get all the posts from the database, sorted with the newest first.

    Returns:
      A list of dictionaries, where each dictionary has a 'content' key
      pointing to the post content, and 'time' key pointing to the time
      it was posted.
    '''

    ## Database connection
    db = psycopg2.connect("dbname=tournament")
    c = db.cursor();
    c.execute("select * from players")
    players = ({'id': str(row[0]), 'name': str(row[1])}
      for row in c.fetchall())
    db.close()
    return players

def getStandings():
    db = psycopg2.connect("dbname=tournament")
    c = db.cursor()
    c.execute("select losses.lossesID as id, name, wins.noOfWins as wins, wins.noOfWins + noOfLosses as no_of_Matches from losses, wins, players where losses.lossesID = wins.winsID and players.id = losses.lossesID order by wins desc;");
    standings = [];
    standings = ({'id': str(row[0]), 'name': str(row[1]), 'wins':str(row[2]), 'matches':str(row[3])}
      for row in c.fetchall())
    db.close()
    return standings

## Add a post to the database.
# def AddPost(content):
#     '''Add a new post to the database.

#     Args:
#       content: The text content of the new post.
#     '''
#     db = psycopg2.connect("dbname=forum")
#     c = db.cursor();
#     c.execute("INSERT INTO posts (content) VALUES (%s)", (content,))
#     db.commit()
#     db.close()
