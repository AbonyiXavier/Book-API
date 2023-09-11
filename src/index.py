from flask import Flask
from os import environ
from dotenv import load_dotenv
from common.constant import API_PREFIX_URL
from domain.user.models.user_model import db
from flask_jwt_extended import JWTManager
from datetime import timedelta
from flask_cors import CORS

# Load environment variables from .env file
load_dotenv()

def create_app():
    app = Flask(__name__)

    CORS(app, resources={rf"{API_PREFIX_URL}/*": {"origins": "*"}}) # set cors

    # Set .env variables
    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')
    app.config['SECRET_KEY'] = environ.get('SECRET_KEY')
    expires_in_seconds = environ.get('JWT_ACCESS_TOKEN_EXPIRES')
    # Convert the string to an integer and then create a timedelta object ;- expires in 2hrs
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(seconds=int(expires_in_seconds))

    db.init_app(app) 
    JWTManager(app)  # Initialize flask_jwt_extended

    with app.app_context():
        # This will create tables based on your models
        db.create_all()  

    return app