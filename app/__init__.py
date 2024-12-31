from flask import Flask
from app.utils.token import jwt
from app.utils.db import db, migrate
from app.config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    with app.app_context():

        from app.models.book_model import Books, Copies, Borrowing, Reserve
        from app.models.libraries_model import Libraries, Location
        from app.models.user_model import User, Report

    return app

__all__ = ["Libraries", "Books", "Copies", "Borrowing", "Reserve", "Location", "User", "Report"]
