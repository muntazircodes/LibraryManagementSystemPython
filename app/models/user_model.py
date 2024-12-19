from app import db
from libraries_model import libraries

# User and Report Model
class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100), nullable=False)
    user_email = db.Column(db.String(100), nullable=False, unique=True)
    user_type = db.Column(db.Enum('admin', 'super_admin', 'user', name='user_type_enum'), nullable=False)
    user_password = db.Column(db.String(100), nullable=False)
    user_verified = db.Column(db.Boolean, default=False, nullable=False)
    lib_id = db.Column(db.Integer, db.ForeignKey('libraries.lib_id'), nullable=False)
    user_fine = db.Column(db.Float, nullable=False)

    # Relationships
    borrowings = db.relationship('Borrowing', back_populates='user', cascade="all, delete-orphan")
    reservations = db.relationship('Reserve', back_populates='user', cascade="all, delete-orphan")


class Report(db.Model):
    __tablename__ = 'report'

    report_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    report_date = db.Column(db.DateTime, nullable=False)
    report_status = db.Column(db.String(100), nullable=False)
    handled_by = db.Column(db.String(100), nullable=False)
    handled = db.Column(db.Boolean, default=False, nullable=False)

    # Relationships
    user = db.relationship('User', back_populates='reports')
