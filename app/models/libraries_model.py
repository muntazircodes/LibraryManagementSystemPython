from app.utils.db import db
from sqlalchemy import String, Integer, Boolean

class Libraries(db.Model):
    __tablename__ = 'libraries'

    lib_id = db.Column(Integer, primary_key=True, autoincrement=True)
    lib_name = db.Column(String(100), nullable=False)
    lib_location = db.Column(String(100), nullable=False)
    lib_admin = db.Column(String(100), nullable=False)
    lib_email = db.Column(String(100), nullable=False, unique=True)
    lib_licence = db.Column(String(100), nullable=False)
    lib_docs = db.Column(String(100), nullable=False)
    library_verified = db.Column(Boolean, default=False, nullable=False)

    books = db.relationship('Book', back_populates='libraries', cascade="all, delete-orphan")
    locations = db.relationship('Location', back_populates='libraries', cascade="all, delete-orphan") 


class Location(db.Model):
    __tablename__ = 'location'

    loc_id = db.Column(Integer, primary_key=True, autoincrement=True)
    lib_id = db.Column(Integer, db.ForeignKey('libraries.lib_id', ondelete='CASCADE'), nullable=False) 
    block = db.Column(String(100))
    floor = db.Column(String(100))
    room = db.Column(String(100))
    locker = db.Column(String(100))
    rack = db.Column(String(100))

    # Relationships
    library = db.relationship('Libraries', back_populates='locations')
    copies = db.relationship('Copies', back_populates='location', cascade="all, delete-orphan")
