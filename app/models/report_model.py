from app.middleware.db import db
from app.enums import ReportStatusEnum
from sqlalchemy import String, Integer, DateTime, ForeignKey, Text, sql

class Report(db.Model):
    __tablename__ = 'reports'

    report_id = db.Column(Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(Integer, ForeignKey('users.user_id'), nullable=False)
    subject = db.Column(String(100), nullable=False)
    message = db.Column(Text, nullable=False)
    report_status = db.Enum(ReportStatusEnum, nullable=False, default=ReportStatusEnum.UNSEEN) 
    handled_by = db.Column(String(100), nullable=False)
    report_date = db.Column(DateTime, server_default=sql.func.now(), nullable=False)

    user = db.relationship('User', back_populates='reports')