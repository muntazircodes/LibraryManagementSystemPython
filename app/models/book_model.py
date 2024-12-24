from app.utils.db import db
from sqlalchemy import Enum


# Book and Copies Model
class Book(db.Model):
    __tablename__ = 'books'

    book_id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(100), nullable=False)
    book_image = db.Column(db.String(100))
    author = db.Column(db.String(100), nullable=False)
    publisher = db.Column(db.String(100), nullable=False)
    book_genre = db.Column(db.String(100), nullable=False)
    edition = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(100), nullable=False, unique=True)
    price = db.Column(db.Float, default=0.0, nullable=False)
    book_stock = db.Column(db.Integer)
    available_stock = db.Column(db.Integer)
    lib_id = db.Column(db.Integer, db.ForeignKey('libraries.lib_id'), nullable=False)

    # Relationships
    library = db.relationship('Libraries', back_populates='books')
    copies = db.relationship('Copies', back_populates='book', cascade="all, delete-orphan")


class Copies(db.Model):
    __tablename__ = 'copies'

    copy_id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'), nullable=False)
    loc_id = db.Column(db.Integer, db.ForeignKey('location.loc_id'), nullable=False)
    copy_status = db.Column(db.String(100), default="Available", nullable=False)
    copy_condition = db.Column(Enum("Excellent", "Good", "Damaged", "Torn"), default="Excellent", nullable=False)
    copy_location = db.Column(db.String(100))
    copy_available = db.Column(Enum("Yes", "No"), default="Yes", nullable=False)
    copy_remarks = db.Column(db.String(100))

    # Relationships
    book = db.relationship('Book', back_populates='copies')
    location = db.relationship('Location', back_populates='copies')
    borrowings = db.relationship('Borrowing', back_populates='copy', cascade="all, delete-orphan")
    reservations = db.relationship('Reserve', back_populates='copy', cascade="all, delete-orphan")


class Borrowing(db.Model):
    __tablename__ = 'borrowings'

    borrow_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    copy_id = db.Column(db.Integer, db.ForeignKey('copies.copy_id'), nullable=False)
    borrow_date = db.Column(db.DateTime, server_default=db.func.current_timestamp(), nullable=False)
    return_date = db.Column(db.DateTime, nullable=False)
    fine = db.Column(db.Float, default=0, nullable=False)

    # Relationships
    user = db.relationship('User', back_populates='borrowings')
    copy = db.relationship('Copies', back_populates='borrowings')


class Reserve(db.Model):
    __tablename__ = 'reserves'

    reserve_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    copy_id = db.Column(db.Integer, db.ForeignKey('copies.copy_id'), nullable=False)
    reserve_time = db.Column(db.DateTime, server_default=db.func.current_timestamp(), nullable=False)
    receiving_time = db.Column(db.DateTime, server_default=db.func.current_timestamp(), nullable=False)
    is_expired = db.Column(db.Boolean, default=False, nullable=False)

    # Relationships
    user = db.relationship('User', back_populates='reservations')
    copy = db.relationship('Copies', back_populates='reservations')
    # C:\Users\munta\.vscode\LmsBackend> 