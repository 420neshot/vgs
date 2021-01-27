from app import app
from flask import render_template, request, jsonify
import requests
import os


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/add_message', methods=['POST'])
def add_message():
    card = request.form['card']
    date = request.form['date']
    cvv = request.form['cvv']

    response = requests.post("https://%s.sandbox.verygoodproxy.com/post" % os.environ.get('VAULT'),
                             json={'card_number': card,
                                   'card_exp': date,
                                   'card_cvc': cvv})

    # converting resonse
    x = response.json()['data']
    x = x.split("\"")
    card = x[3]
    date = x[7]
    cvv = x[11]

    return render_template('message.html', card=card, date=date, cvv=cvv)


@app.route("/forward", methods=['POST'])
def forward():
    card = request.form['card']
    date = request.form['date']
    cvv = request.form['cvv']

    user = os.environ.get('USERNAME')
    pwd = os.environ.get('PASSWORD')
    vault = os.environ.get('VAULT')

    os.environ['HTTPS_PROXY'] = 'https://%s:%s@%s.SANDBOX.verygoodproxy.com:8080' % (user, pwd, vault)
    res = requests.post('https://echo.apps.verygood.systems/post',
                        json={'card_number': card,
                              'card_exp': date,
                              'card_cvc': cvv},
                        verify='/home/oneshot/simple_app_test_vgs-master/sandbox.pem')

    res = res.json()
    return render_template('forward.html', response=res)
