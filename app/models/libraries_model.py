from app.utils.db import db
from sqlalchemy import String, Integer, Boolean
from sqlalchemy.orm import relationship

class Libraries(db.Model):
    __tablename__ = 'libraries'

    lib_id = db.Column(Integer, primary_key=True, autoincrement=True)
    lib_name = db.Column(String(100), nullable=False)
    lib_adress = db.Column(String(100), nullable=False)
    lib_admin = db.Column(String(100), nullable=False)
    lib_email = db.Column(String(100), nullable=False, unique=True)
    lib_licence = db.Column(String(100), nullable=False, unique=True)
    lib_docs = db.Column(String(100), nullable=False)
    library_verified = db.Column(Boolean, default=False, nullable=False)

    books = relationship('Books', back_populates='library', cascade="all, delete-orphan")
    rack = relationship('Racks', back_populates='library', cascade="all, delete-orphan") 


class Racks(db.Model):
    __tablename__ = 'rack'

    rack_id = db.Column(Integer, primary_key=True, autoincrement=True)
    lib_id = db.Column(Integer, db.ForeignKey('libraries.lib_id', ondelete='CASCADE'), nullable=False) 
    block = db.Column(String(100))
    floor = db.Column(String(100))
    room = db.Column(String(100))
    locker = db.Column(String(100))
    rack_no = db.Column(String(100))

    # Relationships
    library = relationship('Libraries', back_populates='rack')
    copies = relationship('Copies', back_populates='rack', cascade="all, delete-orphan")
