from app.utils.db import db
from sqlalchemy import String, Integer, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.types import Enum

class Book(db.Model):
    __tablename__ = 'books'

    book_id = db.Column(Integer, primary_key=True, autoincrement=True)
    book_name = db.Column(String(100), nullable=False)
    volume = db.Column(String(100))
    author = db.Column(String(100), nullable=False)
    publisher = db.Column(String(100), nullable=False)
    book_genre = db.Column(String(100), nullable=False)
    edition = db.Column(String(100), nullable=False)
    isbn = db.Column(String(100), nullable=False, unique=True)
    price = db.Column(Float, default=0.0, nullable=False)
    book_image = db.Column(String(100))
    book_stock = db.Column(Integer, default=0, nullable=False)
    available_stock = db.Column(Integer, nullable=False)
    lib_id = db.Column(Integer, ForeignKey('libraries.lib_id'), nullable=False)
    
    library = db.relationship('Libraries', back_populates='books')
    copies = db.relationship('Copies', back_populates='book', cascade="all, delete-orphan")


class Copies(db.Model):
    __tablename__ = 'copies'

    copy_id = db.Column(Integer, primary_key=True)
    book_id = db.Column(Integer, ForeignKey('books.book_id'), nullable=False)
    loc_id = db.Column(Integer, ForeignKey('location.loc_id'), nullable=False)
    copy_status = db.Column(String(100), default="Available", nullable=False)
    copy_condition = db.Column(Enum("Excellent", "Good", "Damaged", "Torn"), default="Excellent", nullable=False)
    copy_location = db.Column(String(100))
    copy_available = db.Column(Enum("Yes", "No"), default="Yes", nullable=False)
    copy_remarks = db.Column(String(100))

    location = db.relationship('Location', back_populates='copies', lazy='joined') 
    borrowings = db.relationship('Borrowing', back_populates='copy', cascade="all, delete-orphan")
    reservations = db.relationship('Reserve', back_populates='copy', cascade="all, delete-orphan")


class Borrowing(db.Model):
    __tablename__ = 'borrowings'

    borrow_id = db.Column(Integer, primary_key=True)
    user_id = db.Column(Integer, ForeignKey('users.user_id'), nullable=False)
    copy_id = db.Column(Integer, ForeignKey('copies.copy_id'), nullable=False)
    borrow_date = db.Column(DateTime, server_default=db.func.current_timestamp(), nullable=False)
    return_date = db.Column(DateTime)

    user = db.relationship('User', back_populates='borrowings')  
    copy = db.relationship('Copies', back_populates='borrowings')


class Reserve(db.Model):
    __tablename__ = 'reserves'

    reserve_id = db.Column(Integer, primary_key=True)
    user_id = db.Column(Integer, ForeignKey('users.user_id'), nullable=False)
    copy_id = db.Column(Integer, ForeignKey('copies.copy_id'), nullable=False)
    reserve_time = db.Column(DateTime, server_default=db.func.current_timestamp(), nullable=False)
    receiving_time = db.Column(DateTime, default=None)
    is_expired = db.Column(Boolean, default=False, nullable=False)

    user = db.relationship('User', back_populates='reservations')  
    copy = db.relationship('Copies', back_populates='reservations')
