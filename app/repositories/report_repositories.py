from app.utils.db import db
from app.models import Report
class ReportRepository:

    @staticmethod
    def delete_report(report_id):
        report = Report.query.get(report_id)
        db.session.delete(report)
        db.session.commit()


    @staticmethod
    def get_report_by_id(report_id):
        return Report.query.get(report_id)


    @staticmethod
    def get_report_by_user_id(user_id):
        return Report.query.filter_by(user_id=user_id).all()


    @staticmethod
    def mark_report_handled(report_id, handled_by):
        report = Report.query.get(report_id)
        report.handled = True
        report.handled_by = handled_by
        db.session.commit()


    @staticmethod
    def create_report(user_id, subject, message, handled_by=None, handled=False):
        new_report = Report(
            user_id=user_id,
            subject=subject,
            message=message,
            handled_by=handled_by,
            handled=handled
        )
        db.session.add(new_report)
        db.session.commit()
        return new_report    

    @staticmethod
    def update_report(report_id, **kwargs):
        report = Report.query.get(report_id)
        if not report:
            raise ValueError("Report not found")

        allowed_fields = ['subject', 'message', 'handled_by', 'handled']
        try:
            for key, value in kwargs.items():
                if key in allowed_fields and hasattr(report, key):
                    setattr(report, key, value)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        return report    