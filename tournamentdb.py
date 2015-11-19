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

def getSwissPairings():
    standingsList = getStandings()
    # pairingsList = []

    # for i in range(0,len(standingsList)):
    #     if(i%2 == 0):
    #         thisTuple = ({'playerOneID':standingsList[i][0],'playerOneName':standingsList[i][1],'playerTwoId':standingsList[i+1][0],'playerTwoName':standingsList[i+1][1]})
    #         pairingsList.append(thisTuple)
    # return pairingsList

    # works
    # for row in standingsList:
    #   firstRowId = row['id']
    #   print firstRowId

    # standingsList1
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
