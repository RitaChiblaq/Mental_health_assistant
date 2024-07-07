from flask import Flask
from .db_config import Config  # Import the configuration settings from the db_config module
from .models import Base, engine  # Import the SQLAlchemy base and engine


def create_app():
    """
    Creates and configures a Flask application instance.

    Returns:
        Flask app instance.
    """
    app = Flask(__name__)  # Initialize the Flask application
    app.config.from_object(Config)  # Load configuration settings from Config class

    # Initialize the database by creating all tables defined in models
    Base.metadata.create_all(engine)

    return app  # Return the Flask application instance