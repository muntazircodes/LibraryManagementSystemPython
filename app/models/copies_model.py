from app.utils.db import db
from sqlalchemy import String, Integer, ForeignKey
from app.enums import CopyConditionEnum, CopyAvaliabilityEnum


class Copies(db.Model):
    __tablename__ = 'copies'

    copy_id = db.Column(Integer, primary_key=True)
    book_id = db.Column(Integer, ForeignKey('books.book_id'), nullable=False)
    rack_id = db.Column(Integer, ForeignKey('rack.rack_id'), nullable=False)
    copy_condition = db.Enum(CopyConditionEnum, default=CopyConditionEnum.EXCELENT, nullable=False)
    copy_rack = db.Column(String(100))
    copy_available = db.Enum(CopyAvaliabilityEnum, default=CopyAvaliabilityEnum.YES, nullable=False)
    copy_remarks = db.Column(String(100))

    
    rack = db.relationship('Racks', back_populates='copies', lazy='joined') 
    books = db.relationship('Books', back_populates='copies')  
    borrowings = db.relationship('Borrowing', back_populates='copy', cascade="all, delete-orphan")
    reservations= db.relationship('Reserve', back_populates='copy', cascade="all, delete-orphan")
