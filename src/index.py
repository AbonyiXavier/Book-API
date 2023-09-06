from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import environ
from dotenv import load_dotenv
from domain.user.models.user_model import db

# Load environment variables from .env file
load_dotenv()

def create_app():
    app = Flask(__name__)

    # Set the SQLAlchemy database URI here
    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')

    db.init_app(app) 

    with app.app_context():
        # This will create tables based on your models
        db.create_all()  

    return app