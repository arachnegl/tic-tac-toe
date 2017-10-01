from flask import Flask, request

from game_tree import tic_tac_toe


app = Flask(__name__)


@app.route("/hi")
def hello():
    return "Hello World!"


@app.route("/")
def game():
    game = request.args.get('game')
    return tic_tac_toe(game)
