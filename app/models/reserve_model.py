from app.utils.db import db
from sqlalchemy import Integer, DateTime,ForeignKey, Boolean, sql


class Reserve(db.Model):
    __tablename__ = 'reserves'

    reserve_id = db.Column(Integer, primary_key=True)
    user_id = db.Column(Integer, ForeignKey('users.user_id'), nullable=False)
    copy_id = db.Column(Integer, ForeignKey('copies.copy_id'), nullable=False)
    reserve_time = db.Column(DateTime, server_default= sql.func.current_timestamp(), nullable=False)
    receiving_time = db.Column(DateTime, default=None)
    is_expired = db.Column(Boolean, default=False, nullable=False)

    user = db.relationship('User', back_populates='reservations')  
    copy = db.relationship('Copies', back_populates='reservations')