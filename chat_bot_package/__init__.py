from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '0650c9411b66221d947b0ea065d18008'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
pass_crypt = Bcrypt(app)
login_manager = LoginManager(app)

from chat_bot_package import app_routes
