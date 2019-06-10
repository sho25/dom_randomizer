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

    def __init__(self, card_id, name_j, name_e, kana, extension, cost, potion, neg_cost, card_class, card_type):
        self.card_id = card_id
        self.name_j = name_j
        self.name_e = name_e
        self.kana = kana
        self.extension = extension
        self.cost = cost
        self.potion = potion
        self.neg_cost = neg_cost
        self.card_class = card_class
        self.card_type = card_type
    def debug(self):
        print("{},{},{}".format(self.name_j, self.cost, self.extension))

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
    extensions = request.form.getlist("extensions")
    options = request.form.getlist("options")
    print(extensions)
    print(options)

    # 選択した拡張のカードをDBから所得
    ext_cards = [] # 均等配分用
    all_cards = [] # 全ランダム用
    for ext in extensions:
        query_result = db.session.query(CardData).filter(CardData.extension == ext)
        cards = []
        for card in query_result:
            cards.append(Card(card.name_j, card.kana, card.cost, card.extension, card.card_type))
            # card.debug()
        all_cards.extend(cards)
        ext_cards.append(cards)

    # ランダマイズ部分
    randomizer = []
    if 'equal' in options:
        ave_num = math.floor(10 / len(extensions)) 
        for i in range(len(extensions)):
            if i == 0:
                randomizer.extend(random_gen(ext_cards[i], ave_num + 1))
            else:
                randomizer.extend(random_gen(ext_cards[i], ave_num))
    else:
        randomizer.extend(random_gen(all_cards, 10))
    print(randomizer)
        
    return render_template('index.html', extensions=_extensions.extensions, randomizer=randomizer, selected="True", options=_options.options)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
