from app.utils.db import db
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, Text, ForeignKey
from sqlalchemy.types import Enum
from sqlalchemy.sql import func


class User(db.Model):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(100), nullable=False)
    user_email = Column(String(255), nullable=False, unique=True)
    user_password = Column(String(100), nullable=False)
    user_type = Column(Enum('Admin', 'Super Admin', 'User', name='user_type'), nullable=False, server_default='User')
    user_verified = Column(Boolean, server_default='false', nullable=False)
    phone_number = Column(String(20), nullable=True)
    profile_picture = Column(String(255), nullable=True)
    lib_id = Column(Integer, ForeignKey('libraries.lib_id'), nullable=False)
    allowed_books = Column(Integer, server_default='4', nullable=False)
    alloted_books = Column(Integer, server_default='0', nullable=False)
    user_fine = Column(Float, server_default='0.0', nullable=False)
    DOJ = Column(DateTime, server_default=func.now(), nullable=False)
    # Relationships
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
    handled = Column(Boolean, server_default='false', nullable=False)
    report_date = Column(DateTime, server_default=func.now(), nullable=False)

    # Relationships
    user = db.relationship('User', back_populates='reports')
