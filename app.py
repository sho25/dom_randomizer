from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

import main.extensions as _extensions
import main.options as _options

import math
import os
import random
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)

class CardData(db.Model):
    __tablename__ = "card_data"
    card_id = db.Column(db.Integer, primary_key=True)
    name_j = db.Column(db.String(20))
    name_e = db.Column(db.String(30))
    kana = db.Column(db.String(20))
    extension = db.Column(db.String(10))
    cost = db.Column(db.String(10))
    potion = db.Column(db.String(10))
    neg_cost = db.Column(db.String(10))
    card_class = db.Column(db.String(10))
    card_type = db.Column(db.String(20))

class Card():
    def __init__(self, name_j, kana, cost, extension, card_type):
        self.name_j = name_j
        self.kana = kana
        self.cost = cost
        self.extension = extension
        self.card_type = card_type
    def debug(self):
        print("{},{},{}".format(self.name_j, self.cost, self.extension))

def random_gen(list, num):
    random.seed(datetime.now())
    eval = []
    gen_list = []
    for i in range(num):
        rand = random.randrange(len(list))
        while(rand in eval):
            rand = random.randrange(len(list))
        eval.append(rand)
        gen_list.append(list[rand])
    return gen_list

@app.route('/', methods=['GET'])
def index():
    extensions = _extensions.extensions
    options = _options.options
    return render_template('index.html', extensions=extensions, options=options)

@app.route('/', methods=['POST'])
def result():
    post_extensions = request.form.getlist("extensions")
    post_options = request.form.getlist("options")

    # 選択した拡張のカードをDBから所得
    ext_cards = [] # 均等配分用
    all_cards = [] # 全ランダム用
    for ext in post_extensions:
        query_result = db.session.query(CardData).filter(CardData.extension == ext)
        cards = []
        for card in query_result:
            cards.append(Card(card.name_j, card.kana, card.cost, card.extension, card.card_type))
            # card.debug()
        all_cards.extend(cards)
        ext_cards.append(cards)

    # 選択なしj
    if len(post_extensions) == 0:
        return render_template('index.html', extensions=_extensions.extensions, options=_options.options, error="select at least one extension")

    # ランダマイズ部分
    randomizer = []
    if 'equal' in post_options:
        if len(post_extensions) > 10:
            return render_template('index.html', extensions=_extensions.extensions, options=_options.options, error="too many extensions selected", checked=post_extensions)
        
        # とりあえず均等に枚数を選ぶ
        ave_num = math.floor(10 / len(post_extensions)) 
        for i in range(len(post_extensions)):
            randomizer.extend(random_gen(ext_cards[i], ave_num))
        remain = 10 - ave_num*len(post_extensions)
        # 10枚になるまで選ぶ
        # TODO:
        # ランダムでやるとすでに選んだカードがでるので選んだカードは選択肢から外した方がいい
        while remain > 0:
            rand = random.randrange(len(post_extensions))
            gen = random_gen(ext_cards[rand], 1)
            if gen in randomizer:
                continue
            randomizer.extend(gen)
            remain -= 1
    else:
        randomizer.extend(random_gen(all_cards, 10))

    randomizer = sorted(randomizer, key=lambda x: x.cost)
    return render_template('index.html', extensions=_extensions.extensions, randomizer=randomizer, selected="True", options=_options.options, checked=post_extensions)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
