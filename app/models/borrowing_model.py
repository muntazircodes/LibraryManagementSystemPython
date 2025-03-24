from app.middleware.db import db
from sqlalchemy import Integer, DateTime,ForeignKey, sql

class Borrowing(db.Model):
    __tablename__ = 'borrowings'

    borrow_id = db.Column(Integer, primary_key=True)
    user_id = db.Column(Integer, ForeignKey('users.user_id'), nullable=False)
    copy_id = db.Column(Integer, ForeignKey('copies.copy_id'), nullable=False)
    borrow_date = db.Column(DateTime, server_default=sql.func.current_timestamp(), nullable=False)
    return_date = db.Column(DateTime)

    user = db.relationship('User', back_populates='borrowings')  
    copy = db.relationship('Copies', back_populates='borrowings')