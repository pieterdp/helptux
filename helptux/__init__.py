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

from helptux.views.api import *
from helptux.views.admin.auth import *
from helptux.views.admin.user import *
from helptux.views.admin.post import *


@app.route('/')
@app.route('/index')
@app.route('/home')
def v_index():
    return render_template('indexpage.html')


@app.route('/about')
def v_about():
    return ''


@app.route('/contact')
def v_contact():
    return ''


@app.route('/blog')
def v_blog():
    return ''
