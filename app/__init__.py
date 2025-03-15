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
        from app.models.book_model import Books
        from app.models.libraries_model import Libraries
        from app.models.user_model import User
        from app.models.borrowing_model import Borrowing
        from app.models.copies_model import Copies
        from app.models.report_model import Report
        from app.models.racks_model import Racks
        from app.models.reserve_model import Reserve

        from app.routes.auth.register import register_bp
        from app.routes.auth.login import auth_bp

        app.register_blueprint(register_bp)
        app.register_blueprint(auth_bp)
        
    return app


__all__ = ["Libraries", "Books", "Copies", "Borrowing", "Reserve", "Racks", "User", "Report"]
