from app.utils.db import db
from app.models.user_model import User, Report
from app.repositories.library_repository import LibraryRepository


class UserRepository:   

    @staticmethod
    def add_user (
        user_name, user_email, user_password, lib_id, 
        phone_number, valid_docs
    ):
        if User.query.filter_by(user_email=user_email).first():
            raise ValueError("User with this email already exists")

        if not LibraryRepository.library_exists(lib_id):
            raise ValueError("Library with this ID does not exist")

        new_user = User(
            user_name=user_name,
            user_email=user_email,
            user_password=user_password, 
            lib_id=lib_id,
            phone_number=phone_number,
            valid_docs=valid_docs,
        )
        db.session.add(new_user)
        db.session.commit()
        return new_user
    

    @staticmethod
    def update_user(user_id, **kwargs):
        user = User.query.get(user_id)
        if not user:
            raise ValueError("User not found")

        allowed_fields = [
            'user_name', 'user_email', 'user_password', 'user_type', 
            'user_verified', 'user_fine', 'phone_number', 
            'profile_picture', 'allowed_books', 'alloted_books'
        ]
        try:
            for key, value in kwargs.items():
                if key in allowed_fields and hasattr(user, key):
                    setattr(user, key, value)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        return user

    @staticmethod
    def delete_user(user_id):
        user = User.query.get(user_id)
        db.session.delete(user)
        db.session.commit()

    @staticmethod
    def is_admin(user_id):
        user = User.query.get(user_id)
        return user.user_type == 'Admin'
    
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
    def check_user_fine(user_id):
        user = User.query.get(user_id)
        return user.user_fine if user else None
    
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
    
    @staticmethod
    def promote_as_admin(user_id):
        user = User.query.get(user_id)
        user.user_type = 'admin'
        db.session.commit()

    @staticmethod     
    def get_library_admin():
        return User.query.filter_by(user_type='admin').all()
    
    @staticmethod
    def user_borrowings(user_id):
        user = User.query.get(user_id)
        return user.alloted_books 
    
    @staticmethod
    def add_user_allowed_books(user_id, allowed_books):
        user = User.query.get(user_id)
        user.allowed_books += allowed_books
        db.session.commit()


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