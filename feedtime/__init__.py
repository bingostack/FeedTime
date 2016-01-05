#!/usr/bin/python
from flask import Flask, render_template, url_for
from pinterest.pinterest import pinterest

app = Flask(__name__)

app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='2\x8f\xc3+\x8b\xf2H[\x1a\xcd\xa0\xdd\xb0<s\xcc\x10\x94\x05\xf5\xf1\xd0\xbf['
))

app.register_blueprint(pinterest)

@app.route('/')
def index():
    return 'This is stormgiant' + url_for('feedtime_index')

@app.route('/feedtime')
def feedtime_index():
    return render_template('feedtime.html')

