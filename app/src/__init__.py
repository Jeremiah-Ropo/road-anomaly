from flask import Flask
from .config import Config
from .mongo import init_mongo, mongo  # Ensure you import `mongo` here

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    init_mongo(app)  # Initialize Mongo with the app

    with app.app_context():
        from .routes import main as main_blueprint
        app.register_blueprint(main_blueprint)

        from .models import init_db
        init_db()  # Initialize the DB

        from .errors import register_error_handlers
        register_error_handlers(app)

    return app


