import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config as Config
from flask_restful import Api
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
api = Api()
jwt = JWTManager()

def create_app(config):
    app = Flask(__name__)
    config_name = config
    app.config.from_object(Config[config_name])
    db.init_app(app)

    from .account.views import accout
    from .models import Users, Posts
    app.register_blueprint(accout, url_prefix='/account')
    api.init_app(app)
    jwt.init_app(app)

    return app


