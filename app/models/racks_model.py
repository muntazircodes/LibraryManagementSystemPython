from app.utils.db import db
from sqlalchemy import String, Integer

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
    library = db.relationship('Libraries', back_populates='rack')
    copies = db.relationship('Copies', back_populates='rack', cascade="all, delete-orphan")