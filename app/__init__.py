from flask import Flask
from app.utils.db import db, migrate
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  

    db.init_app(app)
    migrate.init_app(app, db)

    return app
