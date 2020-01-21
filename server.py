#!/usr/bin/env python
# -*- coding: utf-8 -*-

#       _                              
#      | |                             
#    __| |_ __ ___  __ _ _ __ ___  ___ 
#   / _` | '__/ _ \/ _` | '_ ` _ \/ __|
#  | (_| | | |  __/ (_| | | | | | \__ \
#   \__,_|_|  \___|\__,_|_| |_| |_|___/ .
#
# A 'Fog Creek'–inspired demo by Kenneth Reitz™

import os
from flask import Flask, request, render_template, jsonify

# Support for gomix's 'front-end' and 'back-end' UI.
app = Flask(__name__, static_folder='public', template_folder='views')

# Set the app secret key from the secret environment variables.
app.secret = os.environ.get('SECRET')

# Comment 'database'. Store in memory for now. 
COMMENTS = ['This game is WICKED HARD.']

# TODO: let's just keep the top 10 scores...

#LEADERBOARD is a list of player objects with name and score
class Player:
  def __init__(self, playername, score):
    self.playername = playername
    self.score = score
    
LEADERBOARD = [Player("Mickey Mouse", 100), Player("Petunia Pig", 50 )]  
    
HIGHSCORE = 0
QUALIFYINGSCORE = 0

# current player stored in memory
PLAYER = "PYTHON FAN"

# Read scores from the file into a list of Player Objects stored in LEADERBOARD
def readscores():
    global LEADERBOARD
    LEADERBOARD = []
    with open("leaderboard.txt", 'r', newline='\n') as leader_file:
      for line in leader_file:        
        record = line.split("|")
        entry = Player(record[0],int(record[1]))
        LEADERBOARD.append(entry)
        LEADERBOARD.sort(key=lambda player: player.score, reverse=True)
        # for debugging purposes: print the entry to console
        print(entry.playername + ":" + str(entry.score))
      
    filterLeaderboard()  
    #readleaderboard()
    
def filterLeaderboard():
    global LEADERBOARD
    global HIGHSCORE
    global QUALIFYINGSCORE
    
    HIGHSCORE = LEADERBOARD[0].score
    QUALIFYINGSCORE = LEADERBOARD[9].score
    print("High Score: " + str(HIGHSCORE) + " Qualifying Score: " + str(QUALIFYINGSCORE))
    qualified_scores = []
    for entry in LEADERBOARD:
      if entry.score >= QUALIFYINGSCORE:
        qualified_scores.append(entry)
    LEADERBOARD = qualified_scores
    
    #TODO: rewrite file to only keep the qualifying scores

# this function will only write to the console, can use for debugging
def readleaderboard():
  print("Reading the Leaderboard:")
  for entry in LEADERBOARD:
    print(entry.playername + str(entry.score))

def writescore(name, score): 
    with open("leaderboard.txt", 'a') as leader_file:
      leader_file.write(name + '|' + score + '|\n')     

@app.after_request
def apply_kr_hello(response):
    """Adds some headers to all responses."""
  
    # Made by Kenneth Reitz. 
    if 'MADE_BY' in os.environ:
        response.headers["X-Was-Here"] = os.environ.get('MADE_BY')
    
    # Powered by Flask. 
    response.headers["X-Powered-By"] = os.environ.get('POWERED_BY')
    return response

@app.route('/')
def homepage():     
    """Displays the homepage."""
    readscores()
    return render_template('index.html', player=PLAYER)
    
#ephemeral memory - broken?
@app.route('/comments', methods=['GET', 'POST'])
def comments():
    # Add a comment to the in-memory database, if given. 
    if 'comment' in request.args:
        COMMENTS.append(request.args['comment'])
    
    # Return the list of remembered comments. 
    return jsonify(COMMENTS)

#User data posted to /user is in the form obect
@app.route('/user', methods=['GET', 'POST'])
def user():
    global PLAYER
    global LEADERBOARD
    # Keep current player name in memory. 
    # TO DO: update Player in index template
    if request.method == 'POST':
        PLAYER = request.form['user']
        score = request.form['score']
        writescore(PLAYER, score) 
        LEADERBOARD.append(Player(PLAYER, int(score))) 
        
        return "Congratulations " + PLAYER + " on your score of: " + score
   
  
#Refresh the in-memory LEADERBOARD with permanent data from file
#Return formatted list to client
@app.route('/leaderboard', methods=['GET', 'POST'])
def leaderboard(): 
    global LEADERBOARD
    readscores()
    # Return the list of remembered leaders and scores 
    results = []
    for entry in LEADERBOARD:
      results.append(entry.playername + ': ' + str(entry.score))
    print(results)
    return jsonify(results)

if __name__ == '__main__':
    app.run()