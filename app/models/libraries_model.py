from app.middleware.db import db
from sqlalchemy import String, Integer
from app.enums.libraray_status_enum import LibraryStatusEnum

class Libraries(db.Model):
    __tablename__ = 'libraries'

    lib_id = db.Column(Integer, primary_key=True, autoincrement=True)
    lib_name = db.Column(String(100), nullable=False)
    lib_address = db.Column(String(100), nullable=False)
    lib_admin = db.Column(String(100), nullable=False)
    lib_email = db.Column(String(100), nullable=False, unique=True)
    lib_license = db.Column(String(100), nullable=False, unique=True)
    lib_docs = db.Column(String(100), nullable=False)
    library_verified = db.Enum(LibraryStatusEnum, default=LibraryStatusEnum.UNVERIFIED, nullable=False)

    books = db.relationship('Books', back_populates='library', cascade="all, delete-orphan")
    rack = db.relationship('Racks', back_populates='library', cascade="all, delete-orphan") 
