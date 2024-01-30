from app.extensions import db
from app.models import *
from app.routes import root
from config import Config
from flask import Flask


def create_app():
    # print(f"args: {args}")
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(root)  #  Register routes

    with app.app_context():
        db.init_app(app)
        db.create_all()  #  Create database and tables

    return app
