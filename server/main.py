import json
import random

from flask import Flask
from flask import request
from flask.ext.cors import CORS

import models

app = Flask(__name__)
CORS(app)

def elo(winner_elo, loser_elo):
    D = min(400, max(-400, winner_elo - loser_elo))
    K = 20
    p = lambda D: 1. / (1 + 10 ** (- D / 400))
    winner_elo = winner_elo + K * (1 - p(D))
    loser_elo = loser_elo + K * (0 - p(-D))
    return winner_elo, loser_elo

def update_score(winner, loser):
    winner = models.Session.query(models.Images).get(winner)
    loser = models.Session.query(models.Images).get(loser)
    winner.elo, loser.elo = elo(winner.elo, loser.elo)
    models.Session.add_all([winner, loser])
    models.Session.commit()

def get_random_images():
    count = models.Session.query(models.Images).count()
    rand1, rand2 = random.randrange(0, count), random.randrange(0, count)
    img1 = models.Session.query(models.Images)[rand1]
    img2 = models.Session.query(models.Images)[rand2]
    return img1.id, img2.id

@app.route('/back', methods=['GET', 'POST'])
def back():
    if request.method == 'POST' and request.json:
        winner = request.json.get('winner')
        loser = request.json.get('loser')
        if winner and loser:
            update_score(winner, loser)
        return ''

    img1, img2 = get_random_images()
    return json.dumps({'img1': img1, 'img2': img2})


if __name__ == '__main__':
    app.run(debug=True)
