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
    c.execute("select losses.lossesID as id, name, wins.noOfWins as wins, losses.noOfLosses as losses, wins.noOfWins + noOfLosses as no_of_Matches from losses, wins, players where losses.lossesID = wins.winsID and players.id = losses.lossesID order by wins desc;");
    standings = [];
    standings = ({'id': str(row[0]), 'name': str(row[1]), 'wins':str(row[2]), 'losses':str(row[3]), 'matches':str(row[4])}
      for row in c.fetchall())
    db.close()
    return standings

def getSwissPairings():
    standingsList = getStandings()
    pairingsList = []

    player1 = True # are we considering player1 or player2?
    for row in standingsList:
      if(player1):
        playerOneId = row['id']
        playerOneName = row['name']
        player1 = False
      else:
        playerTwoId = row['id']
        playerTwoName = row['name']
        thisTuple = ({'playerOneId':playerOneId,'playerOneName':playerOneName,'playerTwoId':playerTwoId,'playerTwoName':playerTwoName})
        pairingsList.append(thisTuple)
    return pairingsList





# Add a post to the database.
def registerPlayer(name):
    '''Add a new post to the database.

    Args:
      content: The text content of the new post.
    '''
    db = psycopg2.connect("dbname=tournament")
    c = db.cursor();
    c.execute("INSERT INTO players (name) VALUES (%s)", (name,))
    db.commit()
    db.close()
