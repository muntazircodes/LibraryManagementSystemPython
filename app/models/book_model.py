from app.utils.db import db
from sqlalchemy import String, Integer, Float, DateTime, Boolean, ForeignKey

class Books(db.Model):
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
    copies = db.relationship('Copies', back_populates='books', cascade="all, delete-orphan")
