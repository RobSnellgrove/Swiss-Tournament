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
    c.execute("select * from players order by id")
    players = ({'id': str(row[0]), 'name': str(row[1])}
      for row in c.fetchall())
    db.close()
    return players

def GetAllPlayersWithNoMatches():

    ## Database connection
    db = psycopg2.connect("dbname=tournament")
    c = db.cursor();
    c.execute("select * from winLossPlayed where no_of_matches = 0")
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

def getStandingsWithFewestPlayed():
    db = psycopg2.connect("dbname=tournament")
    c = db.cursor()
    c.execute("select * from winLossPlayed where no_of_Matches = (select min(no_of_Matches) from winLossPlayed);");
    standingsWFP = [];
    standingsWFP = ({'id': str(row[0]), 'name': str(row[1]), 'wins':str(row[2]), 'losses':str(row[3]), 'matches':str(row[4])}
      for row in c.fetchall())
    db.close()
    return standingsWFP  

def getSwissPairings():
    standingsList = getStandingsWithFewestPlayed()
    pairingsList = []

    player1 = True # are we considering player1 or player2?
    for row in standingsList:
      if(player1): #Is this row player1 or player2 of a game?
        playerOneId = row['id']
        playerOneName = row['name']
        player1 = False
      else:
        playerTwoId = row['id']
        playerTwoName = row['name']
        thisTuple = ({'playerOneId':playerOneId,'playerOneName':playerOneName,'playerTwoId':playerTwoId,'playerTwoName':playerTwoName}) # compile the tuple
        pairingsList.append(thisTuple) # Add tuple to output list.
        player1 = True # Set back to player1
    return pairingsList #return the list

def deletePlayer(id):
    """Remove all the player records from the database."""
    db = psycopg2.connect("dbname=tournament")
    c = db.cursor()
    c.execute('delete from players where id = %s',(str(id),))
    db.commit()
    db.close()

def deleteAllPlayers():
    db = psycopg2.connect("dbname=tournament")
    c = db.cursor()
    c.execute('delete from matches') # delete matches to remove foreign key dependencies
    c.execute('delete from players')
    db.commit()
    db.close()

def deleteAllMatches():
    """Remove all the match records from the database."""
    db = psycopg2.connect("dbname=tournament")
    c = db.cursor()
    c.execute('delete from matches')
    db.commit()
    db.close()

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
 
    db = psycopg2.connect("dbname=tournament")
    c = db.cursor()
    c.execute("insert into matches (winner, loser) values (%s,%s)",(winner,loser))
    db.commit()
    db.close()  



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

# Add view for winLossPlayed table
def createWinLossPlayed():
    db = psycopg2.connect("dbname=tournament")
    c = db.cursor();
    c.execute("create view winLossPlayed as select losses.lossesID as id, name, wins.noOfWins as wins, losses.noOfLosses as losses, wins.noOfWins+losses.noOfLosses as no_of_Matchesfrom losses, wins, players where losses.lossesID = wins.winsID and players.id = losses.lossesID order by wins desc;")
    db.commit()
    db.close()

    