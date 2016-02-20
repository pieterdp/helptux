from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.init_app(app)
login_manager.login_view = '.v_login'

from helptux.routes import *


@app.route('/')
@app.route('/index')
@app.route('/home')
def v_index():
    return render_template('indexpage.html')
