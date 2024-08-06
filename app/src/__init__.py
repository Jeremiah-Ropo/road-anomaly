from flask import Flask # type: ignore
from flask_pymongo import PyMongo # type: ignore
from .config import Config

mongo = PyMongo()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    mongo.init_app(app)

    with app.app_context():
        # Import routes and models
        from .. import routes, models, errors

    return app

