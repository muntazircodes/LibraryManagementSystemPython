from app.utils.db import db
from sqlalchemy.sql import func
from sqlalchemy import String, Integer, Float, DateTime, ForeignKey
from app.enums import UserRoleEnum, UserStatusEnum



class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(String(100), nullable=False)
    user_email = db.Column(String(255), nullable=False, unique=True)
    user_password = db.Column(String(255), nullable=False)
    
    user_type = db.Enum(UserRoleEnum, nullable=False, server_default=UserRoleEnum.USER)

    user_verified = db.Enum(UserStatusEnum, nullable=False, default=UserStatusEnum.UNVERIFIED) 

    phone_number = db.Column(String(20), nullable=True)
    valid_docs = db.Column(String(255), nullable=True)
    profile_picture = db.Column(String(255), nullable=True)
    lib_id = db.Column(Integer, ForeignKey('libraries.lib_id'), nullable=False)
    
    allowed_books = db.Column(Integer, nullable=False, default=4)
    alloted_books = db.Column(Integer, nullable=False, default=0)
    user_fine = db.Column(Float, nullable=False, default=0.0)
    
    DOJ = db.Column(DateTime, server_default=func.now(), nullable=False) 

    borrowings = db.relationship('Borrowing', back_populates='user', cascade="all, delete-orphan")
    reservations = db.relationship('Reserve', back_populates='user', cascade="all, delete-orphan")
    reports = db.relationship('Report', back_populates='user', cascade="all, delete-orphan")
