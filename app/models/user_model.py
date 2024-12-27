from app.utils.db import db
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
import enum

class UserTypeEnum(enum.Enum):
    Admin = 'Admin'
    SuperAdmin = 'Super Admin'
    User = 'User'

class User(db.Model):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(100), nullable=False)
    user_email = Column(String(255), nullable=False, unique=True)
    user_password = Column(String(100), nullable=False)
    
    user_type = Column(String(50), nullable=False, server_default=UserTypeEnum.User.value)
    
    user_verified = Column(Boolean, nullable=False, default=False) 
    phone_number = Column(String(20), nullable=True)
    profile_picture = Column(String(255), nullable=True)
    lib_id = Column(Integer, ForeignKey('libraries.lib_id'), nullable=False)
    
    allowed_books = Column(Integer, nullable=False, default=4)
    alloted_books = Column(Integer, nullable=False, default=0)
    user_fine = Column(Float, nullable=False, default=0.0)
    
    DOJ = Column(DateTime, server_default=func.now(), nullable=False) 

    borrowings = db.relationship('Borrowing', back_populates='user', cascade="all, delete-orphan")
    reservations = db.relationship('Reserve', back_populates='user', cascade="all, delete-orphan")
    reports = db.relationship('Report', back_populates='user', cascade="all, delete-orphan")

class Report(db.Model):
    __tablename__ = 'report'

    report_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    subject = Column(String(100), nullable=False)
    message = Column(Text, nullable=False)
    handled_by = Column(String(100), nullable=False)
    handled = Column(Boolean, nullable=False, default=False) 
    report_date = Column(DateTime, server_default=func.now(), nullable=False)

    # Relationships
    user = db.relationship('User', back_populates='reports')
