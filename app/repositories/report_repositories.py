from app.middleware.db import db
from app.models import Report
from app.enums import ReportStatusEnum

class ReportRepository:
    
    @staticmethod
    def createReport(user_id, subject, message, handled_by=None, report_status=ReportStatusEnum.UNSEEN):
        new_report = Report(
            user_id=user_id,
            subject=subject,
            message=message,
            handled_by=handled_by,
            report_status=report_status
        )
        db.session.add(new_report)
        db.session.commit()
        return new_report    

    @staticmethod
    def getReportById(report_id):
        return Report.query.get(report_id)

    @staticmethod
    def getUserReport(user_id):
        return Report.query.filter_by(user_id=user_id).all()

    @staticmethod
    def updateReport(report_id, **kwargs):
        report = Report.query.get(report_id)
        if not report:
            raise ValueError("Report not found")

        allowed_fields = ['subject', 'message', 'handled_by', 'report_status']
        try:
            for key, value in kwargs.items():
                if key in allowed_fields and hasattr(report, key):
                    setattr(report, key, value)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        return report    

    @staticmethod
    def markReport(report_id, handled_by=None):
        report = Report.query.get(report_id)
        if report is None:
            return "Report not found"
        
        report.report_status = ReportStatusEnum
        report.handled_by = handled_by
        
        try:
            db.session.commit()
            return report
        except Exception as e:
            db.session.rollback()
            raise e

    # DELETE
    @staticmethod
    def deleteReport(report_id):
        report = Report.query.get(report_id)
        db.session.delete(report)
        db.session.commit()
