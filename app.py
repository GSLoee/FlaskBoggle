from flask import Flask, request, render_template, jsonify, session
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'
boggle_game = Boggle()

@app.route("/")
def homepage():
    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get("highscore", 0)
    num_plays = session.get("num_plays", 0)

    return render_template("index.html", board=board, highscore=highscore, num_plays=num_plays)


@app.route("/check-word")
def check_word():
    """check if the word is in the dictionary"""

    word = request.args["word"]
    board = session["board"]
    response = boggle_game.check_valid_word(board, word)

    return jsonify({'result': response})

@app.route("/score", methods=["POST"])
def post_score():
    """receive score and update number of plays and highscore"""

    score = request.json["score"]
    highscore = session.get("highscore", 0)
    num_plays = session.get("num_plays", 0)

    session['num_plays'] = num_plays + 1
    session['highscore'] = max(score, highscore)

    return jsonify(brokeRecord=score > highscore)