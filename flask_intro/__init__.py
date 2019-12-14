import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail


app = Flask(__name__)
app.config['SECRET_KEY'] = '3b121ade881d2b1fac942595d35b5b7204755e30'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db =SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view='users.login'
login_manager.login_message_category = 'info'

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'sundayafolabi992@gmail.com'
app.config['MAIL_PASSWORD'] = 'password'
mail = Mail(app)

from flask_intro.users.route import users
from flask_intro.posts.route import posts
from flask_intro.main.route import main
from flask_intro.Errors.handlers import errors


app.register_blueprint(errors)
app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)