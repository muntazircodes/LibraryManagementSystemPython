from app.utils.db import db
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from app.enums.user_role_enum import UserRoleEnum
from app.enums.user_status_enum import UserStatusEnum
from sqlalchemy.orm import relationship



class User(db.Model):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(100), nullable=False)
    user_email = Column(String(255), nullable=False, unique=True)
    user_password = Column(String(255), nullable=False)
    
    user_type = Column(String(50), nullable=False, server_default=UserRoleEnum.USER)

    user_verified = Column(UserStatusEnum, nullable=False, default=UserStatusEnum.UNVERIFIED) 

    phone_number = Column(String(20), nullable=True)
    valid_docs = Column(String(255), nullable=True)
    profile_picture = Column(String(255), nullable=True)
    lib_id = Column(Integer, ForeignKey('libraries.lib_id'), nullable=False)
    
    allowed_books = Column(Integer, nullable=False, default=4)
    alloted_books = Column(Integer, nullable=False, default=0)
    user_fine = Column(Float, nullable=False, default=0.0)
    
    DOJ = Column(DateTime, server_default=func.now(), nullable=False) 

    borrowings = relationship('Borrowing', back_populates='user', cascade="all, delete-orphan")
    reservations = relationship('Reserve', back_populates='user', cascade="all, delete-orphan")
    reports = relationship('Report', back_populates='user', cascade="all, delete-orphan")

class Report(db.Model):
    __tablename__ = 'reports'

    report_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    subject = Column(String(100), nullable=False)
    message = Column(Text, nullable=False)
    handled_by = Column(String(100), nullable=False)
    handled = Column(Boolean, nullable=False, default=False) 
    report_date = Column(DateTime, server_default=func.now(), nullable=False)

    user = relationship('User', back_populates='reports')
