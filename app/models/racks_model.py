from app.utils.db import db
from sqlalchemy import String, Integer

class Racks(db.Model):
    __tablename__ = 'rack'

    rack_id = db.Column(Integer, primary_key=True, autoincrement=True)
    lib_id = db.Column(Integer, db.ForeignKey('libraries.lib_id'), nullable=False) 
    block = db.Column(String(100))
    floor = db.Column(String(100))
    room = db.Column(String(100))
    locker = db.Column(String(100))
    rack_no = db.Column(String(100))


    library = db.relationship('Libraries', back_populates='rack', cascade="all, delete-orphan")
    copies = db.relationship('Copies', back_populates='rack', cascade="all, delete-orphan")