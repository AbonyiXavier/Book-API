import os

from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

SQLALCHEMY_TRACK_MODIFICATIONS = False

FLASK_RUN_HOST = os.environ.get("FLASK_RUN_HOST", "0.0.0.0")
FLASK_RUN_PORT = os.environ.get("FLASK_RUN_PORT", 9000)
FLASK_DEBUG = os.environ.get("FLASK_DEBUG", False)

SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")

JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
 # Convert the string to an integer and then create a timedelta object ;- expires in 2hrs
JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=int(os.environ.get("JWT_ACCESS_TOKEN_EXPIRES")))
JWT_TOKEN_LOCATION = ["headers"]

