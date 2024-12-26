from app.utils.db import db
from app.models.user_model import User, Report



class UserRepository:   
    @staticmethod
    def add_user(
        user_name, user_email, user_password, user_type, lib_id, 
        user_fine=0.0, phone_number=None, profile_picture=None, 
        allowed_books=4, alloted_books=0
    ):
        new_user = User(
            user_name=user_name,
            user_email=user_email,
            user_password=user_password, 
            user_type=user_type,
            user_verified=False,
            lib_id=lib_id,
            user_fine=user_fine,
            phone_number=phone_number,
            profile_picture=profile_picture,
            allowed_books=allowed_books,
            alloted_books=alloted_books
        )
        db.session.add(new_user)
        db.session.commit()
        return new_user


    @staticmethod
    def update_user(
        user_id, user_name, user_email, user_password, user_type, 
        user_fine, phone_number=None, profile_picture=None, 
        allowed_books=None, alloted_books=None
    ):
        user = User.query.get(user_id)
        user.user_name = user_name
        user.user_email = user_email
        user.user_password = user_password
        user.user_type = user_type
        user.user_fine = user_fine
        user.phone_number = phone_number
        user.profile_picture = profile_picture
        if allowed_books is not None:
            user.allowed_books = allowed_books
        if alloted_books is not None:
            user.alloted_books = alloted_books
        db.session.commit()


    @staticmethod
    def delete_user(user_id):
        user = User.query.get(user_id)
        db.session.delete(user)
        db.session.commit()


    @staticmethod
    def verify_user(user_id):
        user = User.query.get(user_id)
        user.user_verified = True
        db.session.commit()


    @staticmethod
    def verify_all_at_once():
        users = User.query.all()
        for user in users:
            user.user_verified = True
        db.session.commit()


    @staticmethod
    def update_user_fine(user_id, fine_amount):
        user = User.query.get(user_id)
        user.user_fine = fine_amount
        db.session.commit()


    @staticmethod
    def get_all_users():
        return User.query.all()


    @staticmethod
    def get_defaulter_user():
        return User.query.filter(User.user_fine > 0).all()


    @staticmethod
    def get_unverified_users():
        return User.query.filter_by(user_verified=False).all()


    @staticmethod
    def get_user_by_email(user_email):
        return User.query.filter_by(user_email=user_email).first()


    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(user_id)


    @staticmethod
    def get_user_by_name(user_name):
        return User.query.filter(User.user_name.ilike(f"%{user_name}%")).all()
         


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
