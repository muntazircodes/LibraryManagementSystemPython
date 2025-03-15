from app.utils.db import db
from sqlalchemy.sql import func
from app.enums import ReportStatusEnum
from sqlalchemy import String, Integer, DateTime, ForeignKey, Text

class Report(db.Model):
    __tablename__ = 'reports'

    report_id = db.Column(Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(Integer, ForeignKey('users.user_id'), nullable=False)
    subject = db.Column(String(100), nullable=False)
    message = db.Column(Text, nullable=False)
    handled_by = db.Column(String(100), nullable=False)
    handled = db.Enum(ReportStatusEnum, nullable=False, default=ReportStatusEnum.UNSEEN) 
    report_date = db.Column(DateTime, server_default=func.now(), nullable=False)

    user = db.relationship('User', back_populates='reports')