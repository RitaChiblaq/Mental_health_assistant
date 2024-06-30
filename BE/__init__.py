from flask import Flask
from .config import Config
from .models import Base, engine

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize database
    Base.metadata.create_all(engine)

    return app