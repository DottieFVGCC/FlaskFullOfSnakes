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
LEADERBOARD = ['50 Points - Minnie Mouse']

# current player stored in memory
PLAYER = "PYTHON FAN"

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
    return render_template('index.html', player=PLAYER)
    
#ephemeral memory - broken?
@app.route('/comments', methods=['GET', 'POST'])
def comments():
    # Add a comment to the in-memory database, if given. 
    if 'comment' in request.args:
        COMMENTS.append(request.args['comment'])
    
    # Return the list of remembered comments. 
    return jsonify(COMMENTS)

#ephemeral memory
@app.route('/user', methods=['GET', 'POST'])
def user():
    # Keep current player name in memory. 
    # TO DO: update Player in index template
    if 'user' in request.args:      
        PLAYER = request.args['user']
    # Return the Player Name after updating
    return PLAYER    
  
#persistant storage
@app.route('/leaderboard', methods=['GET', 'POST'])
def leaderboard():
    # Add a high score to the leaderboard 
    if 'highscore' in request.args:
        LEADERBOARD.append(request.args['highscore'])
    
    # Return the list
    return jsonify(LEADERBOARD)


if __name__ == '__main__':
    app.run()