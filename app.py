from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
import main.card_data as card_data

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/', methods=['GET'])
def index():
    extensions = card_data.extensions.extensions
    return render_template('index.html', extensions=extensions)

@app.route('/', methods=['POST'])
def result():
    extensions = request.form.getlist("extensions")
    print(extensions)
    randomizer = ['役人', '地下貯蔵庫', '礼拝堂', '祝祭', '庭園', '研究所', '書庫', '市場', '民兵', '鉱山']
    return render_template('index.html', extensions=extensions, randomizer=randomizer, selected="True")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
