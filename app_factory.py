from flask import Flask
from extensions import db, migrate, cors, jwt
from src.common.constant import API_PREFIX_URL

def create_app():
    app = Flask(__name__)

    app.config.from_object("config")

    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app, resources={rf"{API_PREFIX_URL}/*": {"origins": "*"}})
    jwt.init_app(app) 

    return app