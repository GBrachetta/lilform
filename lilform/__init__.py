import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
mode = 'prod'

if mode == 'dev':
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'SQLALCHEMY_DATABASE_URI')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from lilform import routes