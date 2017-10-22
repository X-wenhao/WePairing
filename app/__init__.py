from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import Config
import os

basedir = os.path.abspath(os.path.dirname(__file__))
dbdir=os.path.join(basedir,'data.db')

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
#db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(Config)
    Config.init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
 #   db.init_app(app)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app