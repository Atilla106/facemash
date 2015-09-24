import json
import random

from flask import Flask
from flask import request, make_response
from flask.ext.cors import CORS

from models import *

app = Flask(__name__)
CORS(app)

def elo(winner_elo, loser_elo):
    D = min(400, max(-400, winner_elo - loser_elo))
    K = 20
    p = lambda D: 1. / (1 + 10 ** (- D / 400))
    winner_elo = winner_elo + K * (1 - p(D))
    loser_elo = loser_elo + K * (0 - p(-D))
    return winner_elo, loser_elo

def update_score(winner, loser, user):
    winner = Session.query(Images).get(winner)
    loser = Session.query(Images).get(loser)
    winner.elo, loser.elo = elo(winner.elo, loser.elo)


    match = Matches()
    match.user = user
    match.winner = winner.id
    match.loser = loser.id

    Session.add_all([winner, loser, match])
    Session.commit()

def get_random_images():
    count = Session.query(Images).count()
    rand1, rand2 = random.randrange(0, count), random.randrange(0, count)
    img1, img2 = Session.query(Images)[rand1], Session.query(Images)[rand2]
    return img1.id, img2.id

@app.route('/back', methods=['GET', 'POST'])
def back():
    user_id = request.cookies.get('user_id')

    if not user_id:
        user = Users()
        Session.add(user)
        Session.commit()
    else:
        user = Session.query(Users).get(int(user_id))

    if request.method == 'POST' and request.json:
        winner = request.json.get('winner')
        loser = request.json.get('loser')
        if winner and loser:
            update_score(winner, loser, user.id)

    img1, img2 = get_random_images()
    response = make_response(json.dumps({'img1': img1, 'img2': img2}))
    response.set_cookie('user_id', str(user.id))
    return response


if __name__ == '__main__':
    app.run(debug=True)
