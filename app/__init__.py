from app.extensions import db
from app.models import *
from app.routes import root
from config import Config
from flask import Flask
from worker import init_celery


def create_app():
    # print(f"args: {args}")
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(root)  #  Register routes

    init_celery(app)

    with app.app_context():
        # Database
        db.init_app(app)
        db.create_all()  #  Create database and tables

    return app
