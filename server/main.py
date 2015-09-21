import json
import random
import logging

from flask import Flask
from flask import request, make_response

import models

app = Flask(__name__, static_folder='../dist', static_path ='')

if not app.debug:
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    app.logger.addHandler(stream_handler)

def elo(winner_elo, loser_elo):
    D = min(400, max(-400, winner_elo - loser_elo))
    K = 20
    p = lambda D: 1. / (1 + 10 ** (- D / 400))
    winner_elo = winner_elo + K * (1 - p(D))
    loser_elo = loser_elo + K * (0 - p(-D))
    return winner_elo, loser_elo


def update_score(winner, loser, userid):
    winner = models.Session.query(models.Images).get(winner)
    loser = models.Session.query(models.Images).get(loser)

    winner.elo, loser.elo = elo(winner.elo, loser.elo)
    match = models.Matches(user=userid, winner=winner.id, loser=loser.id)

    models.Session.add_all([winner, loser, match])
    models.Session.commit()

def get_random_images():
    count = models.Session.query(models.Images).count()
    rand1, rand2 = random.randrange(0, count), random.randrange(0, count)
    img1 = models.Session.query(models.Images)[rand1]
    img2 = models.Session.query(models.Images)[rand2]
    return img1.id, img2.id

@app.route('/back', methods=['POST'])
def back():
    user_id = request.cookies.get('user_id')

    if not user_id:
        user = models.Users()
        models.Session.add(user)
        models.Session.commit()
    else:
        user = models.Session.query(models.Users).get(int(user_id))

    if request.method == 'POST' and request.json:
        winner = request.json.get('winner')
        loser = request.json.get('loser')
        if winner and loser:
            update_score(winner, loser, user.id)

    img1, img2 = get_random_images()
    response = make_response(json.dumps({'img1': img1, 'img2': img2}))
    response.set_cookie('user_id', str(user.id))
    return response

@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run()
