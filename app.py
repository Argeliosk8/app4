from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, login_user
from os import environ

app = Flask(__name__)
app.config['SECRET_KEY'] = 'My_secret'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL') or 'sqlite:///myDB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context().push()

db = SQLAlchemy(app)


@app.route('/home')
@app.route('/')
def index():
    return render_template('index.html')

import routes