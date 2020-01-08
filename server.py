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

# Comment database. Store in memory for now. 
COMMENTS = ['This game is WICKED HARD.']

# let's just keep the top 10 scores...
#Todo: move this to persistant storage
#LEADERBOARD is a dictionary with the player name as key


# current player stored in memory
PLAYER = "PYTHON FAN"
LEADERBOARD = {}

def readscores():
    global LEADERBOARD
    with open("leaderboard.txt", 'r', newline='\n') as leader_file:
      for line in leader_file:        
        record = line.split("|")
        LEADERBOARD[record[0]] = record[1] 

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
        LEADERBOARD[PLAYER] = int(score)       
        return "Congratulations " + PLAYER + " on your score of: " + str(LEADERBOARD[PLAYER])
   
#persistant storage
#@app.route('/leaderboard', methods=['GET', 'POST'])
#def leaderboard():
    # Add a high score to the leaderboard 
    #if 'highscore' in request.args:
    #    LEADERBOARD.append(request.args['highscore'])
    
    # Return the list
   # return jsonify(LEADERBOARD)
  
#ephemeral memory - broken?
@app.route('/leaderboard', methods=['GET', 'POST'])
def leaderboard(): 
    global LEADERBOARD
    readscores()
    # Return the list of remembered leaders and scores 
    return jsonify(LEADERBOARD)

if __name__ == '__main__':
    app.run()