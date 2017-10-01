from flask import Flask, request, abort

from game_tree import tic_tac_toe, State, StateInvalid


app = Flask(__name__)


@app.route("/hi")
def hello():
    return "Hello World!"


@app.route("/")
def game():
    board = request.args.get('board')
    if not board:
        abort(400)
    try:
        State(board)
    except StateInvalid:
        abort(400)
    return tic_tac_toe(board)
